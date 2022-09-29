class UnoException(Exception):
    pass


class NotYourTurnException(UnoException):
    pass


class GameStartedException(UnoException):
    pass


class GameNotStartedException(UnoException):
    pass


class AliasTakenException(UnoException):
    pass


class IllegalMoveException(UnoException):
    pass
