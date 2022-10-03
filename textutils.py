from colorama import Fore, Style
from unotypes import Color, Sign, Card, Observation, GameState


def color_string(string, color: Color):
    if color is None:
        return string
    match color:
        case Color.RED:
            return f"{Fore.RED}{string}{Style.RESET_ALL}"
        case Color.BLUE:
            return f"{Fore.BLUE}{string}{Style.RESET_ALL}"
        case Color.YELLOW:
            return f"{Fore.YELLOW}{string}{Style.RESET_ALL}"
        case Color.GREEN:
            return f"{Fore.GREEN}{string}{Style.RESET_ALL}"


def sign_to_string(sign: Sign):
    match sign:
        case Sign.ZERO:
            return "00"
        case Sign.ONE:
            return "01"
        case Sign.TWO:
            return "02"
        case Sign.THREE:
            return "03"
        case Sign.FOUR:
            return "04"
        case Sign.FIVE:
            return "05"
        case Sign.SIX:
            return "06"
        case Sign.SEVEN:
            return "07"
        case Sign.EIGHT:
            return "08"
        case Sign.NINE:
            return "09"
        case Sign.SKIP:
            return "SK"
        case Sign.REVERSE:
            return "RE"
        case Sign.DRAW_TWO:
            return "+2"
        case Sign.DRAW_FOUR:
            return "+4"
        case Sign.CHANGE_COLOR:
            return "CC"


def card_to_string(card: Card):
    return color_string(sign_to_string(card.sign), card.color)


def print_observation(observation: Observation, player_aliases: list[str]):
    current_player_alias = player_aliases[observation.current_agent_idx]
    next_player_idx = (observation.current_agent_idx + observation.direction) % len(observation.cards_left)
    next_player_alias = player_aliases[next_player_idx]

    print("-----------")
    print(f"{current_player_alias}'s turn. Next player is {next_player_alias} (if no action card is played)\n")

    for alias, cards_left in zip(player_aliases, observation.cards_left):
        print(f"{alias} - {cards_left} cards left")

    print(f"\nTop card: {card_to_string(observation.top_card)}\n")

    print(" ".join(["{:>2}".format(i) for i in range(len(observation.hand))]))
    print(" ".join([card_to_string(card) for card in observation.hand]))

    print("-----------")


def print_gamestate(state: GameState, player_aliases):
    current_player_alias = player_aliases[state.current_agent_idx]
    next_player_idx = (state.current_agent_idx + state.direction) % len(state.hands)
    next_player_alias = player_aliases[next_player_idx]

    print("-----------")
    print(f"{current_player_alias}'s turn. Next player is {next_player_alias} (if no action card is played)\n")

    print(f"Draw pile size: {len(state.draw_pile)}")
    print(f"Discard pile size: {len(state.discard_pile)}")
    print(f"Total hand size: {sum([len(hand) for hand in state.hands])}")
    print(f"Total cards: {len(state.draw_pile) + len(state.discard_pile) + sum([len(hand) for hand in state.hands])}")

    print(f"\nTop card: {card_to_string(state.discard_pile.cards[-1])}\n")

    for alias, hand in zip(player_aliases, state.hands):
        print(f"{alias}: {' '.join([card_to_string(card) for card in hand.cards])}")
