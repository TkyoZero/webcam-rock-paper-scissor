import cv2
import time
import mediapipe as mp

# Import our custom modules
from hand_tracker import HandTracker
import game_utils

# Setup MediaPipe drawing utilities for the skeleton overlay
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def run_game():
    # 1. Initialization
    cap = cv2.VideoCapture(0)  # Open default camera (Index 0)
    tracker = HandTracker()

    # Game State Variables
    # States: "WAITING", "COUNTDOWN", "RESULT"
    current_state = "WAITING"

    start_time = 0
    countdown_duration = 3  # seconds
    result_display_duration = 3  # seconds

    player_score = 0
    computer_score = 0

    # Variables to hold the 'locked in' moves for the Result screen
    final_player_move = ""
    final_computer_move = ""
    game_result = ""

    print("Starting Game Loop. Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # 2. Pre-processing
        # Flip frame horizontally for a "mirror" effect (intuitive for user)
        frame = cv2.flip(frame, 1)

        # Detect hand
        detection_result = tracker.detect_hand(frame)

        # 3. Visual Feedback (Custom Drawing)
        if detection_result and detection_result.hand_landmarks:
            # Get the first hand detected
            hand_landmarks = detection_result.hand_landmarks[0]

            # Draw skeleton connections manually using our constants
            h, w, _ = frame.shape
            for start_idx, end_idx in game_utils.HAND_CONNECTIONS:
                start_p = hand_landmarks[start_idx]
                end_p = hand_landmarks[end_idx]
                cv2.line(
                    frame,
                    (int(start_p.x * w), int(start_p.y * h)),
                    (int(end_p.x * w), int(end_p.y * h)),
                    (0, 255, 0),
                    2,
                )

            # Draw landmark points
            for landmark in hand_landmarks:
                cv2.circle(
                    frame,
                    (int(landmark.x * w), int(landmark.y * h)),
                    5,
                    (0, 0, 255),
                    -1,
                )

        # 4. Logic & State Machine
        # Capture key input ONCE per frame to fix 'q' exit and 'space' detection issues
        key = cv2.waitKey(1) & 0xFF

        # Global Quit Handler (Press 'q' at any time)
        if key == ord("q"):
            break

        if current_state == "WAITING":
            cv2.putText(
                frame,
                "Press SPACE to Start",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                f"Player: {player_score} - CPU: {computer_score}",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )

            # Start game on spacebar using the captured key variable
            if key == ord(" "):
                current_state = "COUNTDOWN"
                start_time = time.time()

        elif current_state == "COUNTDOWN":
            elapsed = time.time() - start_time
            time_left = countdown_duration - elapsed

            if time_left > 0:
                # Show countdown number
                cv2.putText(
                    frame,
                    str(int(time_left) + 1),
                    (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    5,
                    (0, 0, 255),
                    5,
                )
            else:
                # Time is up! Capture current gesture and transition
                current_gesture = "Unknown"
                if detection_result and detection_result.hand_landmarks:
                    current_gesture = game_utils.recognize_gesture(
                        detection_result.hand_landmarks[0]
                    )

                final_player_move = current_gesture
                final_computer_move = game_utils.get_computer_move()

                # If no hand detected, result is invalid
                if final_player_move == "Unknown":
                    game_result = "No Hand Detected!"
                else:
                    game_result = game_utils.determine_winner(
                        final_player_move, final_computer_move
                    )
                    # Update Score
                    if game_result == "Player":
                        player_score += 1
                    elif game_result == "Computer":
                        computer_score += 1

                current_state = "RESULT"
                start_time = time.time()

        elif current_state == "RESULT":
            elapsed = time.time() - start_time
            if elapsed < result_display_duration:
                # Show choices
                cv2.putText(
                    frame,
                    f"You: {final_player_move}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    f"CPU: {final_computer_move}",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

                # Show Winner
                if game_result == "Player":
                    result_color = (0, 255, 0)  # Green
                elif game_result == "Computer":
                    result_color = (0, 0, 255)  # Red
                else:
                    result_color = (255, 255, 0)  # Teal/Yellow for Draw or Error

                cv2.putText(
                    frame,
                    f"Result: {game_result}",
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    result_color,
                    3,
                )
            else:
                # Time is up, go back to waiting
                current_state = "WAITING"

        # 5. Render
        cv2.imshow("Rock Paper Scissors", frame)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_game()
