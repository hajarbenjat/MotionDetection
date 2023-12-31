# Real-Time Motion Detection
![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This program uses the Tkinter library to create a user interface that displays the real-time camera feed. It also detects movements in the video stream using the background subtraction method and draws rectangles around the moving objects.

## Prerequisites

- Python 3.x
- OpenCV
- NumPy
- Pandas
- Pillow

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required libraries using the following command:

```
pip install opencv-python numpy pandas pillow
```

## Usage

1. Run the program using the following command:

```
python motion_detection.py
```

2. The application will open and display the live feed from your camera.
3. Moving objects will be detected and surrounded by a green rectangle.
4. The movement count in the video will be displayed.

## Screenshots
![gui](https://github.com/hajarbenjat/MotionDetection/assets/138059507/b68d730d-4463-437e-b7cc-1c50d808b4fc)

^^ my cat ^^

## Controls

- Press the "Escape" key to exit the application.

## Notes

- Ensure that your camera is properly connected and allowed to be used by the application.
- The program uses the background subtraction algorithm to detect movements. This means any changes in the environment will be considered as movement. Use it in a stable environment for better results.

## Author

This program was written by Hajar Benjat.
