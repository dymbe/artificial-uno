import json
import time

from flask import Flask, Response
import dataclasses
from agents.randomagent import RandomAgent
from unoenv import UnoEnvironment
from unotypes import *

app = Flask(__name__)


def serialize_state(state: GameState, aliases) -> str:
    def trim_none(x):
        return {k: v for (k, v) in x if v is not None}
    return json.dumps({
        "gameWon": state.game_won,
        "topCard": dataclasses.asdict(state.discard_pile.top(), dict_factory=trim_none),
        "hands": [dataclasses.asdict(hand, dict_factory=trim_none)["cards"] for hand in state.hands],
        "currentAgentIdx": state.current_agent_idx,
        "direction": state.direction,
        "scores": state.scores,
        "aliases": aliases
    })


def format_sse(data: str, event=None) -> str:
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


@app.route("/listen", methods=["GET"])
def listen():
    agents = [RandomAgent(f"Player {i}") for i in range(10)]
    env = UnoEnvironment(agents=agents, winning_score=500)

    def stream():
        for state in env:
            data = serialize_state(state, env.aliases)
            yield format_sse(data)
            time.sleep(0.5)

    return Response(stream(), mimetype="text/event-stream")
