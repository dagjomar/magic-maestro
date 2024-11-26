class FingerTracker:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        
    def get_left_index_finger_coordinates(self, detection_result):
        """Extract left index finger coordinates from detection results"""
        if not detection_result or not detection_result.hand_landmarks:
            return None
            
        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        
        for idx, handedness in enumerate(handedness_list):
            if handedness[0].category_name == "Right":  # Flipped due to mirror image
                return hand_landmarks_list[idx][8]  # Index finger tip
        return None 
    
    def get_right_index_finger_coordinates(self, detection_result):
        """Extract right index finger coordinates from detection results"""
        if not detection_result or not detection_result.hand_landmarks:
            return None
            
        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        
        for idx, handedness in enumerate(handedness_list):
            if handedness[0].category_name == "Left":  # Flipped due to mirror image
                return hand_landmarks_list[idx][8]  # Index finger tip
        return None 