import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import os
import time
import numpy as np

class HandTrackerVideoConverter:
    def __init__(self, input_video_path, output_video_path, 
                 landmark_drawer=None, optimize_downscale_factor=1):
        if not os.path.exists(input_video_path):
            raise ValueError(f"Input video file not found: {input_video_path}")
            
        self.cap = cv2.VideoCapture(input_video_path)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) / optimize_downscale_factor)
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / optimize_downscale_factor)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output_writer = cv2.VideoWriter(
            output_video_path, fourcc, self.fps, 
            (self.width, self.height)
        )
        
        self.optimize_downscale_factor = optimize_downscale_factor
        self.landmark_drawer = landmark_drawer
        
        # Initialize MediaPipe
        module_dir = os.path.dirname(os.path.abspath(__file__))
        base_options = python.BaseOptions(
            model_asset_path=os.path.join(module_dir, 'hand_landmarker.task')
        )
        
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.2,
            min_hand_presence_confidence=0.2,
            min_tracking_confidence=0.2
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process_video(self, progress_callback=None):
        """
        Process the entire video file and save to output
        
        Args:
            progress_callback: Optional callback function that takes current_frame 
                             and total_frames as arguments
        """
        frame_count = 0
        
        while self.cap.isOpened():
            success, frame = self.cap.read()
            frame_timestamp_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
            if not success:
                break
                
            # Process frame
            if self.optimize_downscale_factor != 1:
                optimized_frame = cv2.resize(frame, (self.width, self.height))
                detection_result = self._detect_hands(optimized_frame, frame_timestamp_ms)
                # Draw landmarks if drawer is provided
                if self.landmark_drawer:
                    frame = self.landmark_drawer(optimized_frame, detection_result)
            else:
                detection_result = self._detect_hands(frame, frame_timestamp_ms)
                # Draw landmarks if drawer is provided
                if self.landmark_drawer:
                    frame = self.landmark_drawer(frame, detection_result)
            
            # Write processed frame
            self.output_writer.write(frame)
            
            frame_count += 1
            if progress_callback:
                progress_callback(frame_count, self.total_frames)
                
    def _detect_hands(self, frame, timestamp):
        """Process a single frame and detect hands"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB, 
            data=frame_rgb
        )
        return self.detector.detect_for_video(
            mp_image, timestamp
        )

    def release(self):
        """Release all resources"""
        self.detector.close()
        self.cap.release()
        self.output_writer.release()