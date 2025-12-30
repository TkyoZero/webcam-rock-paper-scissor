import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time


class HandTracker:
    def __init__(self, model_asset_path="../data/model/hand_landmarker.task"):
        """
        Initialize the MediaPipe Hand Landmarker.

        Args:
            model_asset_path (str): Path to the .task model file downloaded from Google.
        """
        # Create an options object for the Hand Landmarker
        base_options = python.BaseOptions(model_asset_path=model_asset_path)

        # We want the 'VIDEO' running mode because we are using a webcam stream.
        # This helps the model track hands faster by using previous frame data.
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
        )

        # Create the hand landmarker object, loading the model as specified in the options.
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.last_timestamp_ms = 0

    def detect_hand(self, frame):
        """
        Processes a video frame and returns detection results.

        Args:
            frame: A numpy array representing the image (OpenCV format).

        Returns:
            The detection result object containing landmarks, or None if error.
        """
        # MediaPipe requires the image in RGB format (OpenCV uses BGR by default)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # MediaPipe VIDEO mode requires a timestamp in milliseconds
        # We use time.time() * 1000 to get current ms
        current_timestamp_ms = int(time.time() * 1000)

        # Prevent sending the same timestamp twice (can cause crash in video mode)
        # If the clock hasn't ticked forward yet (current <= last)...
        if current_timestamp_ms <= self.last_timestamp_ms:
            # lie to MediaPipe and say 1ms has passed.
            current_timestamp_ms = self.last_timestamp_ms + 1
        self.last_timestamp_ms = current_timestamp_ms

        # Perform hand detection on the frame
        detection_result = self.landmarker.detect_for_video(
            mp_image, current_timestamp_ms
        )

        return detection_result
