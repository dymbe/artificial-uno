# Artificial-UNO

An UNO-game for AIs.

## Competition

For Knowit Objectnet's internal seminar in Rome. The goal of the competition is to create a program that beats the programs of the other participants in UNO.

### Rules

Uses the standard UNO-rules, see https://en.wikipedia.org/wiki/Uno_(card_game). A few details about the official rules that might be surprising to the average UNO-player:

- The aim of the game is to be the first player to score 500 points.
- Points are achieved by being the first to play all of one's own cards. Points are rewarded based on the amount of cards still held by the other players.
- It is illegal to stack "draw two" or "draw four" cards to defend against your opponent "draw two" or "draw four" cards.
- A player may play a "draw four" card only if that player has no cards matching the current color. It is however allowed to lie and play the "draw four" anyway, but the next player may choose to challenge its use. The player who used the "draw four" must privately show their hand to the challenging player in order to demonstrate that they had no prior matching colored cards. If the challenge is successful, then the challenged player must draw four cards instead and play continues with the challenger. Otherwise, the challenger must draw six cards – the four cards they were already required to draw plus two more cards – and lose their turn.

### How to participate

Create a pull request which adds your agent to the `agent`-folder before 19th of October 23:59.

## Setup

`artificial-uno` uses Python 3.10 features, you therefore need to run it with Python 3.10 or greater.

I also recommend setting up a virtual environment for this project (see [venv](https://docs.python.org/3/library/venv.html)).

After setting up your virtual environment with the correct Python version, install the projects dependencies by running

`pip install -r requirements.txt`

### Test setup

Try running

`python unoenv.py`

from your virtual environment. This should start a game with one player-controlled agent and two agents who make random moves. See their implementation in `agents/textagent.py` and `agents/randomagent.py`.

## Creating your own agent

To create your own agent you need to create a class that extends the `UnoAgent` class (see `agents/unoagent.py`) and implements UnoAgent::get_action. Check out `agents/textagent.py` and `agents/randomagent.py` for examples.

### Testing your agent

Create an instance of your custom agent class and pass it into an `UnoEnvironment`. See the example in the main function of `unoenv.py`.
