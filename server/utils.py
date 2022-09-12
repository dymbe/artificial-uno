import itertools
from unotypes import *


def create_deck() -> list[Card]:
    deck = []

    non_wild_signs = [Sign(sign) for sign in Sign if not Sign(sign).is_wild()]

    for c, s in itertools.product(Color, non_wild_signs):
        if s == Sign.ZERO:
            deck.append(Card(sign=s, color=c))
        else:
            deck.extend([Card(sign=s, color=c) for _ in range(2)])

    # Add wildcards
    deck.extend([Card(sign=Sign.CHANGE_COLOR, color=None) for _ in range(4)])
    deck.extend([Card(sign=Sign.PLUS_FOUR, color=None) for _ in range(4)])

    return deck


def goes_on_top(card: Card, previous_card: Card):
    if previous_card is None:
        return True
    elif card.sign == Sign.PLUS_FOUR or card.sign == Sign.CHANGE_COLOR:
        return True
    elif card.color == previous_card.color:
        return True
    elif card.sign == previous_card.sign:
        return True
    else:
        return False
