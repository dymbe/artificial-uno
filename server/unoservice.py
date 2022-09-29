from threading import Lock

from unoexceptions import *
from unogame import UnoGame
from unotypes import *


class UnoService:
    def __init__(self):
        self.lock = Lock()
        self.player_aliases: list[str] = []
        self.game: UnoGame | None = None
        self.scores: list[int] = []

    def reset(self):
        self.player_aliases = []
        self.game = None
        self.scores = []

    def add_player(self, alias: str):
        if self.game:
            raise GameStartedException("Game has already started")
        if alias in self.player_aliases:
            raise AliasTakenException(f'Alias "{alias}" is already taken')
        self.player_aliases.append(alias)

    def start_game(self):
        player_amount = len(self.player_aliases)
        self.game = UnoGame(player_amount)

    def step(self, agent_idx, action: Action):
        if not self.game:
            raise GameNotStartedException("Game has not started yet")
        self.game.step(agent_idx, action)

    def get_observation(self, agent_idx) -> Observation:
        return self.game.state_log[-1].observe(agent_idx)
