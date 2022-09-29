from unotypes import *
from typing import Literal
from copy import deepcopy


class UnoGame:
    def __init__(self, agent_amount: int, winning_score=500):
        assert 2 <= agent_amount <= 10
        self.agent_amount = agent_amount
        self.winning_score = winning_score
        self.game_won = False
        self.scores = agent_amount * [0]

        self.state_log = None
        self.draw_pile = None
        self.hands = None
        self.discard_pile = None
        self.current_agent_idx = None
        self.direction = None
        self.previously_drawn_card = None
        self.init_round()

    def init_round(self):
        self.state_log: list[GameState] = []

        self.draw_pile = DrawPile()
        self.hands = self.draw_pile.distribute_hands(self.agent_amount)

        # Not proper UNO, but implementation is simpler if top card is always a number card
        while not self.draw_pile.top().is_number:
            self.draw_pile.shuffle()

        self.discard_pile = DiscardPile(initial_card=self.draw_pile.pop())

        self.current_agent_idx = random.randint(0, len(self.hands) - 1)
        self.direction: Literal[-1, 1] = 1
        self.previously_drawn_card: Card | None = None

        self.log_state()

    def gamestate(self) -> GameState:
        return GameState(
            draw_pile=self.draw_pile,
            hands=self.hands,
            discard_pile=self.discard_pile,
            current_agent_idx=self.current_agent_idx,
            direction=self.direction,
            previously_drawn_card=self.previously_drawn_card,
            scores=self.scores
        )

    def step(self, agent_idx, action: Action):
        self.gamestate().assert_valid(agent_idx, action)
        hand = self.hands[agent_idx]

        match action:
            case PlayCard(card):
                hand.remove(card)
                self.discard_pile.stack(card)

                increment = 1
                match card.sign:
                    case Sign.SKIP:
                        increment += 1
                    case Sign.REVERSE:
                        self.direction *= -1
                    case Sign.PLUS_TWO:
                        increment += 1
                        self.draw_cards(self.current_agent_idx + self.direction, 2)
                    case Sign.PLUS_FOUR:
                        increment += 1
                        self.draw_cards(self.current_agent_idx + self.direction, 4)

                if len(hand) == 0:
                    self.scores[self.current_agent_idx] += sum([len(hand) for hand in self.hands])
                    if self.scores[self.current_agent_idx] >= self.winning_score:
                        self.game_won = True
                    else:
                        self.init_round()

                self.next_turn(increment)

            case DrawCard():
                card_list = self.draw_cards(self.current_agent_idx, 1)
                if card_list:
                    self.previously_drawn_card = card_list[0]

            case SkipTurn():
                self.next_turn()

        self.log_state()

    def to_agent_idx(self, idx):
        return idx % len(self.hands)

    def next_turn(self, increment=1):
        self.current_agent_idx = self.to_agent_idx(self.current_agent_idx + self.direction * increment)
        self.previously_drawn_card = None

    def recycle_discard_pile(self):
        self.draw_pile.cards += self.discard_pile.cards[:-1]
        self.draw_pile.shuffle()
        self.discard_pile = DiscardPile(self.discard_pile.top())

    def draw_cards(self, idx: int, amount: int):
        idx = self.to_agent_idx(idx)

        if len(self.draw_pile) < amount:
            self.recycle_discard_pile()

        amount = min(len(self.draw_pile), amount)  # Just in case the draw pile is still not big enough
        cards = self.draw_pile.draw_cards(amount)

        self.hands[idx].add(cards)

        return cards

    def log_state(self):
        self.state_log.append(deepcopy(GameState(
            draw_pile=self.draw_pile,
            hands=self.hands,
            discard_pile=self.discard_pile,
            current_agent_idx=self.current_agent_idx,
            direction=self.direction,
            previously_drawn_card=self.previously_drawn_card,
            scores=self.scores)))

    def new_observations(self, agent_idx) -> list[Observation]:
        for i, state in reversed(list(enumerate(self.state_log))):
            if state.current_agent_idx == agent_idx:
                last_unobserved_idx = len(self.state_log) - i - 1
                break
        else:
            last_unobserved_idx = 0
        return [state.observe(agent_idx) for state in self.state_log[last_unobserved_idx:]]

    def observations(self, agent_idx) -> list[Observation]:
        return [state.observe(agent_idx) for state in self.state_log]

    def last_observation(self, agent_idx) -> Observation:
        return self.state_log[-1].observe(agent_idx)
