from abc import ABC, abstractmethod

from unotypes import Observation, Action


class UnoAgent(ABC):
    def __init__(self, alias):
        self.alias = alias

    """
    Gets the next action from the agent

    Parameters
    ----------
    observations : list[Observation]
        All observations of the game state so far for the current round (not the entire game). 
    
    Returns
    -------
    Action
        The next action
    """
    @abstractmethod
    def get_action(self, observations: list[Observation], **kwargs) -> Action:
        pass
