# TODO
# We can improve this file by adding lots of different utility metrics
# and addons, like
# - getting the angle of the hand
# - getting the open / closed state of thand
# - getting calibrated size of hand open/closed? Perhaps this all needs a separate module
# that deals with calibration and has different things.
# yes, it likely makes sense that each of these addons have their own internal state
# and they might support a more general "calibration window" that they can operate within
# and then we can make a re-usable calibration module that we can use once, that will be able
# to make a calibration window that we can give to other modules

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import time
from .utils.finger_tracker import FingerTracker
import os

class HandTracker:
    def __init__(self, camera_id=1, num_hands=2, width=640, height=480, flip=True, optimize_downscale_factor = 1, show_fps=True, running_mode="IMAGE"):
        # Initialize camera
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.optimize_downscale_factor = optimize_downscale_factor
        self.flip = flip
        self.width = width
        self.height = height
        self.num_hands = num_hands
        
        # Store latest detection result
        self.latest_result = None
        
        module_dir = os.path.dirname(os.path.abspath(__file__))

        # Initialize MediaPipe
        base_options = python.BaseOptions(
            model_asset_path=os.path.join(module_dir, '../models/hand_landmarker.task')
        )

        if (running_mode == "IMAGE"):
            self.running_mode = mp.tasks.vision.RunningMode.IMAGE
        elif(running_mode == "LIVE"):
            self.running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM
        else:
            raise ValueError("bad input")


        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=self.running_mode,
            num_hands=self.num_hands,
            min_hand_detection_confidence=0.9,
            min_hand_presence_confidence=0.9,
            min_tracking_confidence=0.9,
            result_callback=self._update_result if self.running_mode == mp.tasks.vision.RunningMode.LIVE_STREAM else None
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Add FPS tracking
        self.show_fps = show_fps
        self.fps_start_time = time.time()
        self.fps = 0
        self.frame_count = 0

    def _update_result(self, result,
                      output_image: mp.Image, timestamp_ms: int):
        """Callback to store the latest detection result"""
        self.latest_result = result

    def get_frame(self):
        """Get the raw camera frame"""
        success, frame = self.cap.read()
        if not success:
            return None
        if self.flip:
            return cv2.flip(frame, 1)  # Horizontal flip
        else:
            return frame
    
    def get_processed_frame(self):
        """Get the processed frame"""
        frame = self.get_frame()
        detection_result = None
        if frame is None:
            return frame, detection_result
            

        if self.optimize_downscale_factor != 1:
            optimized_frame = np.resize(frame, (int(self.width / self.optimize_downscale_factor), int(self.height / self.optimize_downscale_factor)))
            detection_result = self.process_frame(optimized_frame)
        else:
            # Process frame asynchronously and get latest result
            detection_result = self.process_frame(frame)

        # Add FPS to the frame if enabled
        if self.show_fps:
            cv2.putText(
                frame,
                f"FPS: {self.fps:.1f}",
                (10, 30),  # Position: top-left corner
                cv2.FONT_HERSHEY_SIMPLEX,
                1,  # Font scale
                (0, 255, 0),  # Color: green
                2  # Thickness
            )
        
        return frame, detection_result


    def process_frame(self, frame):
        """Process a frame and trigger hand detection"""
        if frame is None:
            return None
            
        # Update FPS calculation
        if self.show_fps:
            self.frame_count += 1
            elapsed_time = time.time() - self.fps_start_time
            if elapsed_time > 1.0:  # Update FPS every second
                self.fps = self.frame_count / elapsed_time
                self.frame_count = 0
                self.fps_start_time = time.time()
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB, 
            data=frame_rgb
        )
        # Process frame asynchronously if in live mode
        if (self.running_mode == mp.tasks.vision.RunningMode.LIVE_STREAM):
            self.detector.detect_async(
                image=mp_image,
                timestamp_ms=int(time.time() * 1000)
            )
        else:
            result = self.detector.detect(
                image=mp_image,
            )
            self.latest_result = result

        return self.latest_result

    def release(self):
        """Release camera and detector resources"""
        self.detector.close()
        self.cap.release()