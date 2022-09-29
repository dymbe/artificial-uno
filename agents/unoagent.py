from abc import ABC, abstractmethod

from unotypes import Observation, Action


class UnoAgent(ABC):
    def __init__(self, alias):
        self.alias = alias

    @abstractmethod
    def get_action(self, observations: list[Observation], **kwargs) -> Action:
        pass
