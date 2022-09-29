from agents.unoagent import UnoAgent
from unotypes import *
import random


class RandomAgent(UnoAgent):
    def get_action(self, observations, **kwargs) -> Action:
        action_space = observations[-1].action_space()
        play_card_actions = [action for action in action_space if isinstance(action, PlayCard)]
        if play_card_actions:
            return random.sample(play_card_actions, 1)[0]
        else:
            return random.sample(action_space, 1)[0]
