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
    cap = cv2.VideoCapture(0) # Open default camera (Index 0)
    tracker = HandTracker()

    # Game State Variables
    # States: "WAITING", "COUNTDOWN", "RESULT"
    current_state = "WAITING"

    start_time = 0
    countdown_duration = 3 # seconds
    result_display_duration = 3 # seconds

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

        # 3. Visual Feedback (Draw Hand Skeleton)
        if detection_result and detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        # 4. State Machine Logic
        current_time = time.time()

        # --- STATE: WAITING ---
        if current_state == "WAITING":
            # Display instructions
            cv2.putText(frame, "Press SPACE to Start", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Show current score
            score_text = f"Player: {player_score} - CPU: {computer_score}"
            cv2.putText(frame, score_text, (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Check for input to switch state
            key = cv2.waitKey(1) & 0xFF
            if key == 32: # 32 is ASCII for Spacebar
                current_state = "COUNTDOWN"
                start_time = current_time # Reset timer

        # --- STATE: COUNTDOWN ---
        elif current_state == "COUNTDOWN":
            elapsed_time = current_time - start_time
            time_left = countdown_duration - elapsed_time

            if time_left > 0:
                # Display the countdown number (3... 2... 1...)
                # We add +1 and int() to show ceiling (e.g., 2.9s becomes "3")
                count_text = str(int(time_left) + 1)
                cv2.putText(frame, count_text, (250, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
            else:
                # Timer finished! Transition to Capture immediately
                # This is the "Capture" moment

                # Default move if no hand detected
                current_gesture = "Unknown"

                # If we have a hand, analyze it NOW
                if detection_result and detection_result.hand_landmarks:
                    # MediaPipe returns a list of hands, we only take the first one [0]
                    first_hand_landmarks = detection_result.hand_landmarks[0]
                    current_gesture = game_utils.recognize_gesture(first_hand_landmarks)

                # Logic Processing
                final_player_move = current_gesture
                final_computer_move = game_utils.get_computer_move()

                if final_player_move == "Unknown":
                    game_result = "No Hand Detected!"
                else:
                    game_result = game_utils.determine_winner(final_player_move, final_computer_move)

                    # Update Score
                    if game_result == "Player":
                        player_score += 1
                    elif game_result == "Computer":
                        computer_score += 1

                # Switch State
                current_state = "RESULT"
                start_time = current_time # Reset timer for result display

        # --- STATE: RESULT ---
        elif current_state == "RESULT":
            elapsed_time = current_time - start_time

            if elapsed_time < result_display_duration:
                # Show who chose what
                cv2.putText(frame, f"You: {final_player_move}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"CPU: {final_computer_move}", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Show Winner
                if game_result == "Player":
                    result_color = (0, 255, 0) # Green
                elif game_result == "Computer":
                    result_color = (0, 0, 255) # Red
                else:
                    result_color = (255, 255, 0) # Teal/Yellow for Draw or Error

                cv2.putText(frame, f"Result: {game_result}", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, result_color, 3)
            else:
                # Time is up, go back to waiting
                current_state = "WAITING"

        # 5. Render
        cv2.imshow('Rock Paper Scissors', frame)

        # Global Quit Handler (Press 'q' at any time)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
