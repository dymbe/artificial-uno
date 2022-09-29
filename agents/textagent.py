from textutils import print_observation
from unoagent import UnoAgent
from unotypes import *


class TextAgent(UnoAgent):
    def get_action(self, observations, player_aliases=None) -> Action:
        observation = observations[-1]
        action = None
        while action is None or not observation.is_valid_action(action):
            print_observation(observation, player_aliases)
            command = input("Enter command >> ")
            if command.startswith("play "):
                arguments = command.split(" ")[1:]
                card_idx = int(arguments[0])
                color = Color(arguments[1].upper()) if len(arguments) >= 2 else None
                if 0 <= card_idx < len(observation.hand):
                    card = observation.hand.cards[card_idx]
                    if color and card.sign.is_wild:
                        card = Card(card.sign, color)
                    action = PlayCard(card)

            elif command == "draw":
                action = DrawCard()

            elif command == "skip":
                action = SkipTurn()

        return action
