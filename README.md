# Eye-Controlled Mouse with Python

## Overview

This project is a Python-based eye-controlled mouse system that allows users to control the computer cursor using iris tracking and perform mouse clicks through eye-blink detection.

The application uses a webcam to capture real-time images, MediaPipe to detect facial landmarks, OpenCV to process and display video frames, and PyAutoGUI to control the mouse.

This project was developed as a computer vision experiment exploring hands-free human-computer interaction.

## Features

- **Real-time Face Landmark Detection:** Detects facial landmarks using MediaPipe Face Landmarker.
- **Iris Tracking:** Estimates the iris center from detected iris landmarks.
- **Mouse Movement:** Maps the estimated iris position to screen coordinates.
- **Blink Detection:** Calculates an eye aspect ratio to detect eye closure.
- **Click Cooldown:** Introduces a delay between clicks to reduce repeated clicking.
- **Live Camera Preview:** Displays facial landmarks and the eye ratio in real time.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Math
- Time
- OS

## Requirements

- Python 3.10 or a compatible version supported by the installed libraries
- A webcam
- A computer with a graphical desktop environment
- The MediaPipe `face_landmarker.task` model file

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/eye-controlled-mouse.git
```

Navigate to the project directory:

```bash
cd eye-controlled-mouse
```

### 2. Install the dependencies

```bash
pip install opencv-python mediapipe pyautogui
```

### 3. Download the MediaPipe model

Download the `face_landmarker.task` model file from the official MediaPipe documentation:

https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker

Place the model file in the same directory as the Python script.

### 4. Run the application

```bash
python operate_computer_with_eyes.py
```

Make sure your webcam is connected and accessible before running the application.

## How It Works

1. The webcam captures video frames using OpenCV.
2. Each frame is converted to RGB format and passed to MediaPipe Face Landmarker.
3. The application extracts facial and iris landmarks.
4. The average coordinates of the iris landmarks are used to estimate the cursor position.
5. The eye aspect ratio is calculated using selected eye landmarks.
6. When the eye ratio falls below a predefined threshold and the cooldown condition is satisfied, a mouse click is triggered.
7. The processed video frame is displayed in a window.

## Configuration

The following variables control the basic behavior of the application:

| Variable | Description |
|---|---|
| `BLINK_THRESHOLD` | Threshold used to detect eye closure |
| `click_cooldown` | Minimum time interval between clicks, in seconds |
| `num_faces` | Maximum number of faces to detect |
| `screen_w`, `screen_h` | Screen dimensions used for cursor positioning |

These values may require adjustment depending on lighting conditions, camera position, and individual eye characteristics.

## Limitations

- Cursor positioning is based on the estimated iris center and is not a fully calibrated gaze-tracking system.
- Head movement and camera angle may affect cursor accuracy.
- Blink detection may require threshold adjustments for different users.
- The current implementation uses one eye's landmarks to calculate the eye ratio.
- A webcam and a compatible graphical desktop environment are required.

## Future Improvements

- Add a calibration process to improve cursor positioning.
- Implement smoother cursor movement.
- Improve blink detection to distinguish intentional clicks from natural blinking.
- Add support for configurable click gestures.
- Improve robustness under different lighting conditions.

## Disclaimer

This project is an experimental computer vision application intended for educational and development purposes. It is not a certified assistive technology system.

## License

Choose an appropriate open-source license before distributing or reusing this project.

