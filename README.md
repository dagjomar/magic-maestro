# Magic Maestro 🪄✨🎹
Create music like never before—control orchestral expression with the wave of your hand!

# Demo
Check out the Magic Maestro in action.
[Demo Video](https://www.youtube.com/shorts/y1Bmcsmi3AA)

## Overview
Magic Maestro is a gesture-based music controller that transforms your hand movements into dynamic musical expression. Inspired by the ROLI Airwave and other gesture-controlled instruments, this DIY project uses computer vision and MIDI integration to control orchestral instruments in real-time. With just a camera and some Python modules, you can bring music to life like a true maestro conducting an orchestra in thin air.

## Features
- 🎵 Real-Time Gesture Control: Adjust expression, volume, and dynamics seamlessly.
- 🎹 MIDI Integration: Works with popular DAWs like Logic Pro X.
- 🖐️ Hand Tracking: Leverages computer vision for intuitive, natural control.
- ✨ DIY and Open-Source: Build your own Magic Maestro with simple tools and code.


## How It Works
#### Hand Tracking:
Uses mediapipe to detect hand positions and track movements.

#### MIDI Mapping:
Maps gesture data to MIDI values and sends MIDI messages for
volume (CC #7) and expression (CC #11) to your DAW
to control orchestral instruments dynamically.


## Getting Started
#### Requirements
- Python 3.x
- A webcam or built-in camera
- MIDI-compatible DAW (e.g., Logic Pro X)
- Libraries:
- mediapipe (for hand tracking)
- rt-midi (for MIDI integration)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/magic-maestro.git
cd magic-maestro
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your DAW to receive MIDI input.

## Usage
1. Run the script to start the hand-tracking system:
```bash
python magic_maestro.py
```

2. Position your hand in front of the camera and move it up and down to adjust intensity.

Follow on-screen instructions for controling the functionality.


# Potential Improvements / TODOs
- UI for configuring things
- Choose MIDI Channel
- Turn on/off individual effects  (expression, volume, modulation, etc)
- Performance improvements
- Binary installation app

# Contributing
Contributions are welcome! If you have ideas for improvements or new features, feel free to submit a pull request. However, you will not receive commercial rights unless a specific agreement is made. If you  want to become a partner and co-owner of the project, feel free to reach out and pitch yourself :)

# Disclaimer
Magic Maestro is an independent project inspired by various gesture-based controllers, such as - but not limited to - the ROLI Airwave and Leap Motion. This project is not affiliated with or endorsed by any existing corporations, companies or organizations. It is purely a private project owned entirely by Dag Jomar Mersland. All rights reserved for potential future commercial use.

# License
License is provided in the LICENSE.md file.


