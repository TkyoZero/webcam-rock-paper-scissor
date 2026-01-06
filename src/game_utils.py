import random


# fmt: off
# Tuples representing which landmarks connect to form the skeleton
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17)                                # Wrist to Pinky Base
]
# fmt: on


def is_finger_open(landmarks, finger_tip_index, finger_pip_index):
    """
    Determines if a finger is open based on the relative Y-coordinates
    of the tip and the PIP joint (the middle knuckle).

    In computer vision (OpenCV), the Y-axis increases downwards.
    Therefore, a finger is 'up' (Open) if the Tip Y is LESS than the PIP Y.

    Args:
        landmarks: List of NormalizedLandmark objects from MediaPipe.
        finger_tip_index (int): Index of the finger tip landmark.
        finger_pip_index (int): Index of the finger PIP joint landmark.

    Returns:
        bool: True if the finger is open, False if closed.
    """
    finger_tip_y = landmarks[finger_tip_index].y
    finger_pip_y = landmarks[finger_pip_index].y

    # Check if tip is physically higher on screen than the knuckle
    return finger_tip_y < finger_pip_y


def recognize_gesture(landmarks):
    """
    Analyzes hand landmarks to classify the gesture as Rock, Paper, or Scissors.

    Args:
        landmarks: The list of landmarks detected by MediaPipe.

    Returns:
        str: 'Rock', 'Paper', 'Scissors', or 'Unknown'.
    """
    # MediaPipe Landmark Indices:
    # Index Finger:  Tip=8,  PIP=6
    # Middle Finger: Tip=12, PIP=10
    # Ring Finger:   Tip=16, PIP=14
    # Pinky Finger:  Tip=20, PIP=18

    index_is_open = is_finger_open(landmarks, 8, 6)
    middle_is_open = is_finger_open(landmarks, 12, 10)
    ring_is_open = is_finger_open(landmarks, 16, 14)
    pinky_is_open = is_finger_open(landmarks, 20, 18)

    # Logic Table:
    # Rock:     All four fingers are closed.
    # Paper:    All four fingers are open.
    # Scissors: Index and Middle are open; Ring and Pinky are closed.

    if index_is_open and middle_is_open and ring_is_open and pinky_is_open:
        return "Paper"

    elif index_is_open and middle_is_open and not ring_is_open and not pinky_is_open:
        return "Scissors"

    elif (
        not index_is_open
        and not middle_is_open
        and not ring_is_open
        and not pinky_is_open
    ):
        return "Rock"

    else:
        # Any other combination (e.g., just one finger up) is invalid for this game
        return "Unknown"


def get_computer_move():
    """Randomly selects a move for the computer."""
    options = ["Rock", "Paper", "Scissors"]
    return random.choice(options)


def determine_winner(player_move, computer_move):
    """
    Compares moves to determine the winner.

    Returns:
        str: 'Player', 'Computer', or 'Draw'
    """
    if player_move == computer_move:
        return "Draw"

    # Winning conditions for the player
    if (
        (player_move == "Rock" and computer_move == "Scissors")
        or (player_move == "Paper" and computer_move == "Rock")
        or (player_move == "Scissors" and computer_move == "Paper")
    ):
        return "Player"

    return "Computer"
