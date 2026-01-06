# Webcam Rock Paper Scissors

An interactive Rock Paper Scissors game controlled by your hand gestures using a webcam. The project uses Artificial Intelligence (MediaPipe) to recognize your hand gestures in real-time.

## About the Project

This program allows you to play the classic game against the computer without using a keyboard or mouse.

* **Technology:** Python, OpenCV, Google MediaPipe.
* **Control:** Your hand movements are analyzed live.
* **Logic:** A State Machine controls the game flow (Waiting -> Countdown -> Result).

## Project Management with `uv`

This project is managed using [uv](https://github.com/astral-sh/uv "null"), an extremely fast Python package manager and workflow tool.

### Why `uv`?

* **Init** : Standardized project structure defined in `pyproject.toml`.
* **Env** : Automatic management of virtual environments (`.venv`) ensuring project isolation.
* **Lock** : A `uv.lock` file is used to ensure reproducible builds across different machines by pinning exact dependency versions.

## Prerequisites

* **uv** : Ensure you have `uv` installed. If not, install it via:

```
  curl -LsSf https://astral-sh/uv/install.sh | sh
```

* **Hardware** : Integrated or external USB webcam.
* **Model File** : Ensure `hand_landmarker.task` is located at `../data/model/` (or as configured in your code).

## Setup & Installation

1. **Clone the repository** :

```
   git clone <your-repository-url>
   cd webcam-rock-paper-scissor
```

1. **Synchronize the environment** :
   Run the following command to create a virtual environment and install all dependencies exactly as defined in the lockfile:

```
   uv sync
```

## How to Play

1. **Launch the game** :
   Use `uv run` to execute the script within the managed environment:

```
   uv run python main.py
```

   Or use the convenience script defined in `pyproject.toml`:

```
   uv run webcam-rps
```

1. **Controls** :

* **SPACE** : Start a new round.
* **'q'** : Quit the application.

1. **Gameplay** :

* Press **SPACE** to start a 3-second countdown.
* Position your hand in view.
* Show your gesture (Rock, Paper, or Scissors).
* The computer randomly selects its move and the winner is displayed.

* **`main.py`**
  The entry point. This file handles the "Game Loop", draws the window, counts the score, and processes user input (keyboard).
* **`hand_tracker.py`**
  The interface to MediaPipe. This file handles the technical setup of the AI, loading the model, and converting the webcam image for recognition.
* **`game_utils.py`**
  The game logic. This file calculates:
  * Is a finger open or closed? (Geometry)
  * Which gesture is it? (Rock, Paper, Scissors)
  * Who won the round?

## Customization

You can change settings directly in the code:

* **Countdown Duration:** Change the `countdown_duration` variable in `main.py`.
* **New Gestures:** Theoretically, you could add gestures like "Lizard" or "Spock" in `game_utils.py`.
