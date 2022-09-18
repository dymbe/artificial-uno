from sseclient import SSEClient
from unotypes import *
from requests import Session
import json
import sys
from textutils import card_to_string
from dataclasses import asdict

base_url = "http://localhost:5000"


class UnoClient:
    def __init__(self, alias):
        self.alias = alias
        self.session = Session()
        self.join_game()
        self.state = self.get_state()

    def join_game(self):
        data = {"alias": self.alias}
        r = self.session.post(f"{base_url}/join-game", json=data)
        if r.status_code == 200:
            print(f'Joined game as "{self.alias}"')
        elif r.status_code == 409:
            # TODO: Currently assumes 409 means player already joined, make more robust
            print(f'Alias "{self.alias}" already taken. By me?')
        else:
            # TODO: Handle
            print("Something else went bad")

    def get_state(self):
        r = self.session.get(f"{base_url}/partial-state/{self.alias}")
        return state_from_dict(r.json())

    def play_card(self, card):
        payload = json.dumps({
            "alias": self.alias,
            "card": asdict(card)
        })
        headers = {'Content-Type': 'application/json'}
        r = self.session.post(f"{base_url}/play-card", headers=headers, data=payload)
        return r.status_code == 200

    def start_loop(self):
        url = f"{base_url}/listen?alias={self.alias}"
        headers = {'Accept': 'text/event-stream'}
        response = self.session.get(url, stream=True, headers=headers)
        client = SSEClient(response)
        for event in client.events():
            data = json.loads(event.data)
            self.state = state_from_dict(data["state"])
            self.on_update_state()
            if self.state.game_started and self.state.player_aliases[self.state.current_player_idx] == self.alias:
                self.do_stuff()

    def on_update_state(self):
        print("---------")
        self.print_state()
        print("---------")

    def do_stuff(self):
        while True:
            command = input("Enter command >> ")
            if command.startswith("play "):
                hand_idx = int(command[5:])
                if 0 <= hand_idx < len(self.state.hand):
                    card = self.state.hand[hand_idx]
                    if self.play_card(card):
                        return
                    else:
                        print("Something went wrong")
                        continue
                else:
                    continue

    def print_state(self):
        state = self.state
        current_player_alias = state.player_aliases[state.current_player_idx]
        next_player_idx = (state.current_player_idx + state.direction) % len(state.player_aliases)
        next_player_alias = state.player_aliases[next_player_idx]

        print(f"{current_player_alias}'s turn. Next player is {next_player_alias} (if no action card is played)\n")

        for alias, cards_left in zip(state.player_aliases, state.cards_left):
            print(f"{alias} - {cards_left} cards left")

        if state.discard_pile:
            print(f"\nTop card: {card_to_string(state.discard_pile[-1])}\n")
        else:
            print("\nNo card played yet\n")

        if state.hand:
            print(" ".join([f" {i}" for i in range(len(state.hand))]))
            print(" ".join([card_to_string(card) for card in state.hand]))
        else:
            print("No cards in hand")


if __name__ == '__main__':
    alias = sys.argv[1]
    unoclient = UnoClient(alias)
    unoclient.start_loop()
