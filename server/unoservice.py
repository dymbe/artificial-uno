import dataclasses
import random
from threading import Lock
from exceptions import *
from unotypes import *
from utils import create_deck, goes_on_top
from typing import Literal


class UnoService:
    def __init__(self):
        self.lock = Lock()
        self.player_aliases: list[str] = []
        self.hands: list[list[Card]] = []
        self.current_player_idx = 0
        self.direction: Literal[-1, 1] = 1
        self.game_started = False
        self.plus_twos_played = 0   # How PLUS_TWO's have been played and not drawn
        self.draw_pile: list[Card] = create_deck()
        self.discard_pile: list[Card] = []
        random.shuffle(self.draw_pile)

    def add_player(self, alias: str):
        if self.game_started:
            raise GameStartedException("Game has already started")
        elif alias in self.player_aliases:
            raise AliasTakenException(f'Alias "{alias}" is already taken')
        else:
            self.player_aliases.append(alias)
            self.hands.append([])

    def start_game(self):
        if self.game_started:
            raise GameStartedException("Game has already started")
        else:
            for i in range(len(self.hands)):
                self.draw_cards(i, 7)
            self.current_player_idx = 0#random.randint(0, len(self.hands) - 1)
            self.game_started = True

    def make_move(self, player_idx, move: Move):
        if not self.game_started:
            raise GameNotStartedException("Game has not started yet")
        elif self.current_player_idx != player_idx:
            raise NotYourTurnException(f"Current player is {self.player_aliases[self.current_player_idx]}"
                                       f", not {self.player_aliases[player_idx]}")
        match move:
            case PlayCard(card):
                if self.discard_pile:
                    previous_card = self.discard_pile[-1]
                else:
                    previous_card = None
                if card not in self.hands[player_idx]:
                    raise IllegalMoveException("Card not in hand")
                if not card.stacks_on(previous_card):
                    raise IllegalMoveException(f"{card} can not be placed on top of {previous_card}")
                if self.plus_twos_played > 0 and card.sign != Sign.PLUS_TWO:
                    raise IllegalMoveException("Can only play a PLUS_TWO or draw cards, when previous player played a "
                                               "PLUS_TWO")
                self.hands[player_idx].remove(card)
                self.discard_pile.append(card)
                self.next_turn()
                match card.sign:
                    case Sign.SKIP:
                        self.next_turn()
                    case Sign.REVERSE:
                        self.direction *= -1
                    case Sign.PLUS_TWO:
                        self.plus_twos_played += 1
                    case Sign.PLUS_FOUR:
                        self.draw_cards(self.current_player_idx, 4)
                        self.next_turn()

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + self.direction) % len(self.hands)

    def play_card(self, player_idx: int, card: Card) -> list[Card]:
        if not self.game_started:
            raise GameNotStartedException("Game has not started yet")
        if card.color is None:
            raise ValueError("A played card needs to have its color defined")
        elif self.current_player_idx != player_idx:
            raise NotYourTurnException(f"Current player is {self.player_aliases[self.current_player_idx]}"
                                       f", not {self.player_aliases[self.current_player_idx]}")
        elif card not in self.hands[player_idx]:
            raise IllegalMoveException("Card not in hand")
        elif self.draw_counter > 0 and card.sign != Sign.PLUS_TWO:
            raise IllegalMoveException("Can only play a PLUS_TWO when previous player played a PLUS_TWO")
        else:
            if goes_on_top(card, self.discard_pile[-1]):
                self.hands[player_idx].remove(card)
                self.discard_pile.append(card)
        return self.hands[player_idx]

    def recycle_discard_pile(self):
        raise NotImplementedError("FUCKKKKK")

    def draw_cards(self, player_idx: int, amount: int):
        if len(self.draw_pile) < amount:
            self.recycle_discard_pile()

        amount = min(len(self.draw_pile), amount)   # Just in case the draw pile is still not big enough

        self.hands[player_idx].extend(self.draw_pile[-amount:])
        self.draw_pile = self.draw_pile[:-amount]

    def end_turn(self):
        self.current_player_idx += 1

    def restart(self):
        self.__init__()

    def get_partial_game_state(self, player_idx) -> dict:
        return dataclasses.asdict(
            PartialGameState(
                game_started=self.game_started,
                discard_pile=self.discard_pile,
                player_aliases=self.player_aliases,
                hand=self.hands[player_idx],
                cards_left=[len(hand) for hand in self.hands],
                current_player_idx=self.current_player_idx,
                direction=self.direction,
                plus_twos_played=self.plus_twos_played
            )
        )
