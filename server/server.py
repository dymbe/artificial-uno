import json
from flask import Flask, Response, request, send_file
from messageannouncer import MessageAnnouncer
from unoservice import UnoService
from unotypes import *
from exceptions import *

app = Flask(__name__)
announcer = MessageAnnouncer()
unoservice = UnoService()


@app.route("/")
def hello_world():
    return send_file("index.html")


@app.route("/join-game", methods=["POST"])
def join_game():
    alias = request.json["alias"]

    try:
        unoservice.lock.acquire()
        unoservice.add_player(alias)
        announcer.announce(f"{alias} joined the game")
        return {"alias": unoservice.player_aliases}, 200
    except AliasTakenException as e:
        return {"message": str(e)}, 409
    finally:
        unoservice.lock.release()


@app.route("/start-game", methods=["POST"])
def start_game():
    try:
        unoservice.lock.acquire()
        unoservice.start_game()
        announcer.announce("Game started")
        return {}, 200
    except GameStartedException as e:
        return {"message": str(e)}, 403
    finally:
        unoservice.lock.release()


@app.route("/play-card", methods=["POST"])
def play_card():
    body = request.json
    alias = body["alias"]
    sign = Sign(body["card"]["sign"])
    color = Color(body["card"]["color"])
    card = Card(sign, color)
    move = PlayCard(card)

    try:
        unoservice.lock.acquire()
        if alias not in unoservice.player_aliases:
            return {"message": f'"{alias}" not in game'}, 403
        player_idx = unoservice.player_aliases.index(alias)
        unoservice.make_move(player_idx, move)
        announcer.announce(f"{card} played by {alias}")
        state = unoservice.get_partial_game_state(player_idx)
        return {"state": state}, 200
    except IllegalMoveException as e:
        return {"message": str(e)}, 403
    except GameNotStartedException as e:
        return {"message": str(e)}, 403
    finally:
        unoservice.lock.release()


def format_sse(data: str, event=None) -> str:
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


@app.route("/ping")
def ping():
    msg = format_sse(data="pong")
    announcer.announce(msg=msg)
    return {}, 200


@app.route("/listen", methods=["GET"])
def listen():
    alias = request.args.get("alias")

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            try:
                unoservice.lock.acquire()
                player_idx = unoservice.player_aliases.index(alias)
                state = unoservice.get_partial_game_state(player_idx)
                data = json.dumps({
                    "msg": msg,
                    "state": state
                })
                yield format_sse(data)
            finally:
                unoservice.lock.release()

    return Response(stream(), mimetype="text/event-stream")
