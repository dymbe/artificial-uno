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
                idx = self.uno_game.current_agent_idx
                yield idx, self.agents[idx]
            scores = self.uno_game.state_log[-1].scores

            print("Scores:")
            print("\n".join([f"{alias}: {score}" for (alias, score) in zip(self.aliases, self.uno_game.scores)]))
            print(self.print_winner())
        except StopIteration:
            pass

    def step(self, agent_idx: int, action: Action):
        self.uno_game.step(agent_idx, action)

    def new_observations(self, agent_idx) -> list[Observation]:
        return self.uno_game.new_observations(agent_idx)

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

    agents = [RandomAgent(f"Player {i}") for i in range(10)]
    player_aliases = [agent.alias for agent in agents]
    env = UnoEnvironment(agents=agents, winning_score=500)

    for i, (agent_idx, agent) in enumerate(env.agent_iter()):
        observations = env.new_observations(agent_idx)
        action = agent.get_action(observations, player_aliases=player_aliases)
        env.step(agent_idx, action)

    print(i)


if __name__ == '__main__':
    main()
