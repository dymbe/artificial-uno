from agents.unoagent import UnoAgent
from unotypes import *
import numpy as np
import tensorflow as tf
import itertools


play_card_actions: list[Action] = [PlayCard(Card(sign, color)) for sign, color in itertools.product(Sign, Color)]
actions: list[Action] = play_card_actions + [DrawCard(), SkipTurn(), AcceptDrawFour(), ChallengeDrawFour()]
ACTION_SPACE_SIZE = len(actions)


def encode_observation(o: Observation) -> np.ndarray:
    next_agent_idx = (o.current_agent_idx + o.direction) % len(o.cards_left)
    prev_agent_idx = (o.current_agent_idx - o.direction) % len(o.cards_left)

    next_agent_cards_left = o.cards_left[next_agent_idx]
    prev_agent_cards_left = o.cards_left[prev_agent_idx]

    cards_left = len(o.hand)
    wildcard_amount = len([c for c in o.hand if c.is_wild])
    action_card_amount = len([c for c in o.hand if c.is_action])
    playable_cards = len([c for c in o.hand if c.stacks_on(o.top_card)])
    red_cards = len([c for c in o.hand if c.color == Color.RED])
    green_cards = len([c for c in o.hand if c.color == Color.GREEN])
    blue_cards = len([c for c in o.hand if c.color == Color.BLUE])
    yellow_cards = len([c for c in o.hand if c.color == Color.YELLOW])

    score = o.scores[o.agent_idx]

    return np.asarray([
        next_agent_cards_left,
        prev_agent_cards_left,
        cards_left,
        wildcard_amount,
        action_card_amount,
        red_cards,
        green_cards,
        blue_cards,
        yellow_cards,
        playable_cards,
        score
    ])


def mask_illegal_moves(q_values: np.ndarray, o: Observation) -> np.ndarray:
    action_space = o.action_space()
    illegal_action_idxs = [i for i, action in enumerate(actions) if action not in action_space]
    q_values[illegal_action_idxs] = -np.inf
    return q_values


class NaiveDqn(UnoAgent):
    def __init__(self, alias):
        super(NaiveDqn, self).__init__(alias)
        self.model = tf.keras.models.load_model("./agents/models/ContinuedNet__1666230125____12.20avg")

    def get_qs(self, state: np.ndarray):
        return self.model(state.reshape(1, *state.shape))[0].numpy()

    def get_action(self, observations: list[Observation], **kwargs) -> Action:
        current_state = encode_observation(observations[-1])
        q_values = mask_illegal_moves(self.get_qs(current_state), observations[-1])
        action_idx = np.argmax(q_values)
        return actions[action_idx]
