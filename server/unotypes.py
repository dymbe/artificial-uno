from enum import Enum
from dataclasses import dataclass
from typing import Literal


class Color(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"


class Sign(str, Enum):
    ZERO = "ZERO"
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"
    SIX = "SIX"
    SEVEN = "SEVEN"
    EIGHT = "EIGHT"
    NINE = "NINE"
    SKIP = "SKIP"
    REVERSE = "REVERSE"
    PLUS_TWO = "PLUS_TWO"
    PLUS_FOUR = "PLUS_FOUR"
    CHANGE_COLOR = "CHANGE_COLOR"

    def is_wild(self):
        return self == Sign.PLUS_FOUR or self == Sign.CHANGE_COLOR

    def is_action_card(self):
        return (self == Sign.SKIP or
                self == Sign.REVERSE or
                self == Sign.PLUS_TWO or
                self.is_wild())


@dataclass(frozen=True)
class Card:
    sign: Sign
    color: Color | None

    def is_wild(self) -> bool:
        return self.sign.is_wild()

    def stacks_on(self, card):
        return (card is None or
                self.is_wild() or
                self.color == card.color or
                self.sign == card.sign)

    def __post_init__(self):
        if not self.is_wild() and self.color is None:
            raise TypeError("Color can only be None for PLUS_FOUR and CHANGE_COLOR cards")


@dataclass(frozen=True)
class PlayCard:
    card: Card


@dataclass(frozen=True)
class DrawCard:
    pass


@dataclass(frozen=True)
class ChallengePlusFour:
    pass


Move = PlayCard | DrawCard | ChallengePlusFour


@dataclass(frozen=True)
class PartialGameState:
    game_started: bool
    discard_pile: list[Card]
    player_aliases: list[str]
    hand: list[Card]
    cards_left: list[int]
    current_player_idx: int
    direction: Literal[-1, 1]
    plus_twos_played: int
