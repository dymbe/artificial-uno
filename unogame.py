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
        self.can_challenge_draw_four = None
        self.draw_four_stacked_on = None
        self.revealed_hand_idx = None
        self.challenger_idx = None
        self.revealed_hand = None

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

        self.can_challenge_draw_four = False
        self.draw_four_stacked_on: Card | None = None
        self.challenger_idx: int | None = None
        self.revealed_hand_idx: int | None = None
        self.revealed_hand: Hand | None = None

        self.log_state()

    def gamestate(self) -> GameState:
        return GameState(
            game_won=self.game_won,
            draw_pile=self.draw_pile,
            hands=self.hands,
            discard_pile=self.discard_pile,
            current_agent_idx=self.current_agent_idx,
            direction=self.direction,
            previously_drawn_card=self.previously_drawn_card,
            can_challenge_draw_four=self.can_challenge_draw_four,
            draw_four_stacked_on=self.draw_four_stacked_on,
            challenger_idx=self.challenger_idx,
            revealed_hand_idx=self.revealed_hand_idx,
            revealed_hand=self.revealed_hand,
            scores=self.scores
        )

    def step(self, agent_idx, action: Action):
        self.gamestate().assert_valid(agent_idx, action)
        hand = self.hands[agent_idx]

        match action:
            case PlayCard(card):
                increment = 1
                match card.sign:
                    case Sign.SKIP:
                        increment += 1
                    case Sign.REVERSE:
                        self.direction *= -1
                    case Sign.DRAW_TWO:
                        increment += 1
                        self.draw_cards(self.current_agent_idx + self.direction, 2)
                    case Sign.DRAW_FOUR:
                        self.can_challenge_draw_four = True
                        self.draw_four_stacked_on = self.discard_pile.top()

                hand.remove(card)
                self.discard_pile.stack(card)

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

            case AcceptDrawFour():
                self.draw_cards(self.current_agent_idx, 4)
                self.next_turn()

                self.can_challenge_draw_four = False
                self.draw_four_stacked_on = None

            case ChallengeDrawFour():
                self.challenger_idx = self.current_agent_idx
                self.revealed_hand_idx = (self.current_agent_idx - self.direction) % len(self.hands)
                self.revealed_hand = deepcopy(self.hands[self.revealed_hand_idx])

                if any(card.stacks_on(self.draw_four_stacked_on) for card in self.revealed_hand if not card.is_wild):
                    self.draw_cards(self.revealed_hand_idx, 4)
                else:
                    self.draw_cards(self.current_agent_idx, 6)
                    self.next_turn()

                self.can_challenge_draw_four = False
                self.draw_four_stacked_on = None

        self.log_state()

        self.challenger_idx = None
        self.revealed_hand_idx = None
        self.revealed_hand = None

    def next_turn(self, increment=1):
        self.current_agent_idx = (self.current_agent_idx + self.direction * increment) % len(self.hands)
        self.previously_drawn_card = None

    def recycle_discard_pile(self):
        self.draw_pile.cards += self.discard_pile.cards[:-1]
        self.draw_pile.shuffle()
        self.discard_pile = DiscardPile(self.discard_pile.top())

    def draw_cards(self, idx: int, amount: int):
        idx = idx % len(self.hands)

        if len(self.draw_pile) < amount:
            self.recycle_discard_pile()

        amount = min(len(self.draw_pile), amount)  # Just in case the draw pile is still not big enough
        cards = self.draw_pile.draw_cards(amount)

        self.hands[idx].add(cards)

        return cards

    def log_state(self):
        self.state_log.append(deepcopy(self.gamestate()))

    def observations(self, agent_idx) -> list[Observation]:
        return [state.observe(agent_idx) for state in self.state_log]

    def last_observation(self, agent_idx) -> Observation:
        return self.state_log[-1].observe(agent_idx)
