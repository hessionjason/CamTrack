import cv2
import torch
import pygame

# Initialize pygame mixer for sound alerts
pygame.mixer.init()

# Load alert sound (ensure the path is correct)
alert_sound = r'C:\PersonalProjects\pythonProject\SensorSound.mp3'  # Path to your sound file

# Load YOLOv5 model (pretrained)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define distance thresholds (in terms of bounding box size)
NEAR_THRESHOLD = 300  # Very close (large bounding box)
MID_THRESHOLD = 150   # Medium distance
FAR_THRESHOLD = 50    # Far away (small bounding box)

# Open camera (default index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Perform inference on the frame using YOLOv5
    results = model(frame)

    # Extract detections as tensors
    detections = results.xyxy[0]

    # Loop through detections
    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)  # Get bounding box coordinates
        label = results.names[int(cls)]  # Get class label
        confidence = float(conf)

        # Check if the detected object is a 'person' or 'car'
        if label in ['person', 'car']:
            # Draw bounding box and label on the frame
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw blue box
            frame = cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # Label

            # Calculate the bounding box size (used as a proxy for distance)
            bbox_height = y2 - y1  # Height of the bounding box

            # Calculate volume based on proximity (0.0 to 1.0)
            if bbox_height > NEAR_THRESHOLD:
                volume = 1.0  # Full volume for very close objects
                print(f'ALERT! {label} is VERY CLOSE!')
            elif MID_THRESHOLD < bbox_height <= NEAR_THRESHOLD:
                volume = 0.7  # Medium volume for moderately close objects
                print(f'Warning! {label} is moderately close.')
            elif FAR_THRESHOLD < bbox_height <= MID_THRESHOLD:
                volume = 0.4  # Lower volume for far objects
                print(f'{label} detected, distance: Far.')
            else:
                volume = 0.0  # No sound if the object is very far

            # Adjust volume and play alert sound if object is within detection range
            if volume > 0.0:
                pygame.mixer.music.load(alert_sound)
                pygame.mixer.music.set_volume(volume)  # Set the sound volume based on proximity
                pygame.mixer.music.play()

    # Display the frame with bounding boxes and labels
    cv2.imshow('Dashcam Object Detection', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
