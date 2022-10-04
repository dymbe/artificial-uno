# Artificial-UNO

An UNO-game for AIs. Uses the standard UNO-rules. See https://en.wikipedia.org/wiki/Uno_(card_game)

## Setup

`artificial-uno` uses Python 3.10 features, you therefore need to run it with Python 3.10 or greater.

I also recommend setting up a virtual environment for this project (see [venv](https://docs.python.org/3/library/venv.html)).

After setting up your virtual environment with the correct Python version, install the projects dependencies by running

`pip install -r requirements.txt`

### Test setup

Try running

`python unoenv.py`

from your virtual environment. It should start a game with one player agent and two random agents.

## Creating your own agent

To create your own agent you need to create a class that extends the `UnoAgent` class (see `agents/unoagent.py`) and implements UnoAgent::get_action. Check out `agents/textagent.py` and `agents/randomagent.py` for examples.

### Testing your agent

Create an instance of your custom agent class and pass it into an `UnoEnvironment`. See example in `unoenv.py`.

## How to participate

Create a pull request which adds your agent to the `agent`-folder before 19th of October 23:59.
