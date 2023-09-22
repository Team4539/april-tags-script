import cv2
from frc_apriltags import Detector, NetworkCommunications, USBCamera
import numpy as np
from pathlib import Path
# Initialize the AprilTag detector
detector = Detector(6)

# Get the directory path
dirPath = Path(__file__).absolute().parent.__str__()

# Add way to send data to network table

# Open the USB camera
camera = cv2.VideoCapture(0)

# Calibrate Camera
calicamera = USBCamera(0, None, (1280,720), 15, True, dirPath)

net = NetworkCommunications()
while True:
    # Read a frame from the camera
    ret, frame = camera.read()
    if not ret:
        break

    # Convert the frame to grayscale for AprilTag detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the frame
    #detections = detector.detector.detect(gray_frame)
    detections = detector.detectTags(gray_frame, calicamera.getMatrix(), 3)
    # Filter detections based on size and pose
    valid_detections = []
    for detection in detections:
        # Filter out most false positives
        if detection.decision_margin > 0.9:
            # more filtering
            if detection.tag_id is not None:
                # even more filtering
                if detection.hamming < 1:
                    valid_detections.append(detection)

    # Draw rectangles and tag_id text for the valid AprilTags
    for detection in valid_detections:
        for corner in detection.corners:
            cv2.circle(frame, tuple(map(int, corner)), 3, (0, 0, 255), -1)
        cv2.polylines(frame, [np.array(detection.corners, dtype=int)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Calculate the position for the text (below the tag)
        text_x = int(min(detection.corners[:, 0]))
        text_y = int(max(detection.corners[:, 1])) + 20
        
        
        # Draw the tag_id text
        cv2.putText(frame, f"Tag ID: {detection.tag_id}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the frame with valid AprilTag detections
    cv2.imshow('AprilTag Detection', frame)

    # Exit when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
