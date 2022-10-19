from agents.unoagent import UnoAgent
from unotypes import *
import numpy as np
import tensorflow as tf
from collections import deque
from modifiedtensorboard import ModifiedTensorBoard
from time import time
import itertools
from unorlenv import encode_observation


DISCOUNT = 0.7
MAX_REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE = 64
UPDATE_TARGET_EVERY = 10

MODEL_NAME = "ContinuedNet"


play_card_actions: list[Action] = [PlayCard(Card(sign, color)) for sign, color in itertools.product(Sign, Color)]
actions: list[Action] = play_card_actions + [DrawCard(), SkipTurn(), AcceptDrawFour(), ChallengeDrawFour()]
ACTION_SPACE_SIZE = len(actions)


def mask_illegal_moves(q_values: np.ndarray, o: Observation) -> np.ndarray:
    action_space = o.action_space()
    illegal_action_idxs = [i for i, action in enumerate(actions) if action not in action_space]
    q_values[illegal_action_idxs] = -np.inf
    return q_values


class NaiveDqn(UnoAgent):
    def __init__(self, alias):
        super(NaiveDqn, self).__init__(alias)
        self.model = tf.keras.models.load_model("./agents/models/ContinuedNet__1666185727__-215.79avg")

    def get_qs(self, state: np.ndarray):
        return self.model(state.reshape(1, *state.shape))[0].numpy()

    def get_action(self, observations: list[Observation], **kwargs) -> Action:
        current_state = encode_observation(observations[-1])
        q_values = mask_illegal_moves(self.get_qs(current_state), observations[-1])
        action_idx = np.argmax(q_values)
        return actions[action_idx]
