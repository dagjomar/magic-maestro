#!/bin/bash

# This will download the necessary hand landmark model from Google
# and save it in the src/models directory
wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -O src/models/hand_landmarker.task