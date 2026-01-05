# Webcam Rock Paper Scissors

An interactive Rock Paper Scissors game controlled by your hand gestures using a webcam. The project uses Artificial Intelligence (MediaPipe) to recognize your hand gestures in real-time.

## About the Project

This program allows you to play the classic game against the computer without using a keyboard or mouse.

* **Technology:** Python, OpenCV, Google MediaPipe.
* **Control:** Your hand movements are analyzed live.
* **Logic:** A State Machine controls the game flow (Waiting -> Countdown -> Result).

## Installation & Setup

### 1. Prerequisites

You need Python (version 3.8 or higher) and a functioning webcam.

### 2. Install Dependencies

Install the required Python libraries via the terminal:

```
pip install opencv-python mediapipe
```

### 3. Download the AI Model

The project requires a specific MediaPipe model file to detect hands.

1. Create the subfolders in your project directory: `data/model/`
2. Download the file `hand_landmarker.task` (from the official Google MediaPipe website).
3. Save it as: `data/model/hand_landmarker.task`

*Note: The file path in the code (`hand_tracker.py`) is set to this location by default.*

## How to Play

1. Start the program:
   ```
   python src/main.py
   ```
2. Hold your hand in front of the camera until you see the green skeleton overlay on your hand.
3. Press the **SPACE BAR** to start the game.
4. A countdown begins: **3... 2... 1...**
5. At "1", show your gesture (Rock, Paper, or Scissors).
6. The result and the winner are displayed immediately.
7. Press **'q'** to quit the program.

## Project Structure

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
