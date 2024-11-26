from hand_tracking.hand_tracker import HandTracker
from hand_tracking.utils import FingerTracker
from hand_tracking.utils import LandmarkDrawer
from hand_tracking.utils import lerp, inverse_lerp, clamp
import cv2
from midi import MidiManager
import mediapipe.python.solutions.drawing_utils as drawing_utils
import numpy as np
import os

video_frame_size = (608, 1080)
video_filename = "video_out.mp4"

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc('M','J','P','G'),
    'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

def main():
    tracker = HandTracker(
        camera_id=1,
        show_fps=True,
        flip=False,
        running_mode="LIVE",
        width=video_frame_size[0],
        height=video_frame_size[1],
        optimize_downscale_factor=1,
        num_hands=1,
    )

     # Initialize utilities
    finger_tracker = FingerTracker(tracker)

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

    landmark_drawer = LandmarkDrawer(tracker=tracker, landmark_style=custom_landmark_style, connection_style=custom_connection_style)
    midi_manager = MidiManager()

    # out = cv2.VideoWriter(video_filename, get_video_type(video_filename), 30, video_frame_size, isColor=True)
    
    try:
        while True:
            # Get and process frame
            frame, detection_result = tracker.get_processed_frame()

            if frame is not None:

                landmark_image = landmark_drawer.draw_landmarks(
                    frame=frame,
                    detection_result=detection_result,
                    copy=True,
                    keepOriginal=False,
                    hand_filter="Right"
                )
                # frame = landmark_drawer.draw_landmarks(frame=frame, detection_result=detection_result, copy=False)
                video_frame = landmark_image
                # Show frame
                # Get left index finger coordinates
                coordinates = finger_tracker.get_left_index_finger_coordinates(detection_result)
                if coordinates:
                    min_value = 0.8
                    relative_value = inverse_lerp(0, min_value, min_value-coordinates.y)
                    amplitude = clamp(0, 1, relative_value)
                    midi_value = lerp(0, 127, amplitude)
                    midi_manager.send_expression(midi_value)
                    midi_manager.send_volume(midi_value)

                # Ensure frame size matches VideoWriter dimensions
                # video_frame = np.copy(video_frame)
                # video_frame = cv2.resize(video_frame, video_frame_size)
                # out.write(video_frame)
                cv2.imshow('Hand Tracking', landmark_image)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # out.release()
        tracker.release()
        midi_manager.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()