import cv2
import torch
import pandas as pd  # Ensure pandas is imported to prevent future errors
import requests  # Ensure requests is imported to prevent future errors
from PIL import Image  # Ensure Pillow is imported to prevent future errors

# Load YOLOv5 model (small version for fast detection)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open camera (default index 0)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Perform inference on the frame
    results = model(frame)

    # Draw results on the frame
    frame = results.render()[0]  # Render the bounding boxes on the frame

    # Display the frame with detections
    cv2.imshow('Dashcam Object Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
