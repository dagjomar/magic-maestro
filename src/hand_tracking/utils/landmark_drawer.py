import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

class LandmarkDrawer:
    def __init__(self, tracker=None, landmark_style=None, connection_style=None):
        self.tracker = tracker
        self.landmark_style = landmark_style
        self.connection_style = connection_style

    def draw_landmarks(self, frame, detection_result, copy=False, keepOriginal=True, hand_filter=None):
        """
        Draw landmarks on the frame
        Args:
            frame: Input image frame
            detection_result: MediaPipe hand detection results
            copy: Whether to create a copy of the frame
            keepOriginal: Whether to keep the original frame or create a transparent one
            hand_filter: Optional filter for 'Left' or 'Right' hand
        """

        if (frame is None) or (keepOriginal is False):
            # Create a blank transparent image to draw on
            height, width = frame.shape[:2]
            annotated_image = np.zeros((height, width, 3), dtype=np.uint8)
            # Make the image transparent
            annotated_image[:, :, 2] = 0
        else:    
            # Create a copy of the frame to draw on
            if copy:
                annotated_image = np.copy(frame)
            else:
                annotated_image = frame
        
        # Draw landmarks if we have detection results
        if detection_result and detection_result.hand_landmarks:
            for idx, (hand_landmarks, handedness) in enumerate(zip(detection_result.hand_landmarks, 
                                                                 detection_result.handedness)):
                # Skip if hand_filter is set and doesn't match current hand
                current_hand = handedness[0].category_name  # 'Left' or 'Right'
                if hand_filter and current_hand != hand_filter:
                    continue
                    
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) 
                    for landmark in hand_landmarks
                ])
                
                solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    hand_landmarks_proto,
                    solutions.hands.HAND_CONNECTIONS,
                    self.landmark_style or solutions.drawing_styles.get_default_hand_landmarks_style(),
                    self.connection_style or solutions.drawing_styles.get_default_hand_connections_style()
                )
        
        
        return annotated_image