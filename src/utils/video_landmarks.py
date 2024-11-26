# This script is used to convert an existing video file to a video file with hand landmarks drawn on it

from hand_tracking import HandTrackerVideoConverter
import cv2
import numpy as np
import argparse
import os
from hand_tracking.utils import LandmarkDrawer
import mediapipe.python.solutions.drawing_utils as drawing_utils

# Create custom drawing styles
custom_landmark_style = drawing_utils.DrawingSpec(
    color=(255, 100, 255),  # Pink
    thickness=8,
    circle_radius=6
)

custom_connection_style = drawing_utils.DrawingSpec(
    color=(255, 200, 250),
    thickness=5
)

landmark_drawer = LandmarkDrawer(landmark_style=custom_landmark_style, connection_style=custom_connection_style)

def draw_landmarks(frame, detection_result):
    """Draw landmarks and connections on the frame"""
    landmark_frame = landmark_drawer.draw_landmarks(
        frame=frame,
        detection_result=detection_result,
        copy=False,
        keepOriginal=False,
        hand_filter="Right"
    )

    return landmark_frame

def print_progress(current, total):
    """Print progress percentage"""
    percentage = (current / total) * 100
    print(f"\rProcessing: {percentage:.1f}%", end="")

def main():
    # parser = argparse.ArgumentParser(description='Process video with hand tracking')
    # parser.add_argument('input', help='Input video file path')
    # parser.add_argument('output', help='Output video file path')
    # parser.add_argument('--optimize', type=float, default=1.0,
    #                   help='Downscale factor for optimization (e.g., 2.0 for half resolution)')
    # args = parser.parse_args()

    # Configure input/output paths
    input_video = os.path.join("/path/to/video.mov")
    output_video = os.path.join("/path/to/output.mp4")

    print("input_video", input_video)

    # Create converter with our custom landmark drawer
    converter = HandTrackerVideoConverter(
        # input_video_path=args.input,
        input_video_path=input_video,
        # output_video_path=args.output,
        output_video_path=output_video,
        landmark_drawer=draw_landmarks,
        # optimize_downscale_factor=1
    )

    try:
        print(f"Processing video: {input_video}")
        print(f"Output will be saved to: {output_video}")
        converter.process_video(progress_callback=print_progress)
        print("\nProcessing complete!")
    finally:
        converter.release()

if __name__ == "__main__":
    main()