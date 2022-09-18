from colorama import Fore, Style
from unotypes import Color, Sign, Card


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
        case Sign.PLUS_TWO:
            return "+2"
        case Sign.PLUS_FOUR:
            return "+4"
        case Sign.CHANGE_COLOR:
            return "CC"


def card_to_string(card: Card):
    return color_string(sign_to_string(card.sign), card.color)
