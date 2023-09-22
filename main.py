import cv2
from frc_apriltags import Detector, NetworkCommunications, USBCamera, startNetworkComms, Logger
import numpy as np
from pathlib import Path

# Stop logger from being annoying PLEASE

# Initialize the AprilTag detector
detector = Detector(6)

# Get the directory path
dirPath = Path(__file__).absolute().parent.__str__()

# Add way to send data to network table
startNetworkComms(4539)
net = NetworkCommunications()

# Open the USB camera
camera = cv2.VideoCapture(0)

# Calibrate Camera
calicamera = USBCamera(0, None, (1280,720), 15, True, dirPath)

while True:
    # Read a frame from the camera
    ret, frame = camera.read()
    if not ret:
        break

    # Convert the frame to grayscale for AprilTag detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the frame
    result, stream = detector.detectTags(gray_frame, calicamera.camMatrix, 2)

    for tag in result:
        if tag[0] != None:
            net.setTargetValid(True)
            tag_id = tag[0]
            tag_pos = tag[1]
        else:
            net.setTargetValid(False)

    # Display the frame with valid AprilTag detections
    cv2.imshow('AprilTag Detection', stream)

    # Exit when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
