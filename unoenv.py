from agents.unoagent import UnoAgent
from unogame import UnoGame
from unotypes import *
from textutils import print_gamestate


class UnoEnvironment:
    def __init__(self, agents, winning_score=500):
        self.agents: list[UnoAgent] = agents
        self.aliases = [agent.alias for agent in self.agents]
        self.uno_game = UnoGame(len(agents), winning_score=winning_score)

    def agent_iter(self):
        try:
            while not self.uno_game.game_won:
                agent_idx = self.uno_game.current_agent_idx
                yield agent_idx, self.agents[agent_idx]
        except StopIteration:
            pass

    def __iter__(self):
        yield self.uno_game.gamestate()
        for agent_idx, agent in self.agent_iter():
            observations = self.observations(agent_idx)
            action = agent.get_action(observations, aliases=self.aliases)
            try:
                self.step(agent_idx, action)
            except Exception as e:
                print(e)
                print("Invalid action:", action)
                action = observations[-1].action_space().intersection([DrawCard(), SkipTurn(), AcceptDrawFour()]).pop()
                self.step(agent_idx, action)
            yield self.uno_game.gamestate()

    def step(self, agent_idx: int, action: Action):
        self.uno_game.step(agent_idx, action)

    def observations(self, agent_idx) -> list[Observation]:
        return self.uno_game.observations(agent_idx)

    def print_state(self):
        print_gamestate(self.uno_game.state_log[-1], self.aliases)

    def print_winner(self):
        if self.uno_game.game_won:
            winner_idx = next(i for (i, score) in
                              enumerate(self.uno_game.scores)
                              if score > self.uno_game.winning_score)
            winner_alias = self.aliases[winner_idx]
            print(f"THE WINNER IS {winner_alias}!!!!")
        else:
            print("No winner yet")


def main():
    from agents.randomagent import RandomAgent
    from agents.textagent import TextAgent

    agents = [TextAgent("Player"), RandomAgent("RandomAgent 1"), RandomAgent("RandomAgent 2")]
    env = UnoEnvironment(agents=agents, winning_score=500)
    for i, state in enumerate(env):
        if state.game_won:
            print(state.scores)
            env.print_winner()


if __name__ == '__main__':
    main()
