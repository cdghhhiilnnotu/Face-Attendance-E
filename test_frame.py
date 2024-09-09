# import cv2
# import time

# # Open a connection to the camera
# cap = cv2.VideoCapture(1)

# # Initialize variables to calculate FPS
# prev_frame_time = 0
# new_frame_time = 0

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Calculate FPS
#     new_frame_time = time.time()
#     fps = 1 / (new_frame_time - prev_frame_time)
#     prev_frame_time = new_frame_time

#     # Convert FPS to integer and display on frame
#     fps = int(fps)
#     fps = str(fps)
#     cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

#     # Display the resulting frame
#     cv2.imshow('Frame', frame)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()

import cv2
import torch
from tinyfaces import TinyFaces

# Load the pre-trained Tiny Face Detector model
model = TinyFaces()
model.load_state_dict(torch.load('path_to_pretrained_weights.pth'))
model.eval()

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert frame to tensor
    input_tensor = torch.from_numpy(rgb_frame).permute(2, 0, 1).unsqueeze(0).float()

    # Detect faces
    with torch.no_grad():
        detections = model(input_tensor)

    # Draw rectangles around detected faces
    for detection in detections:
        x, y, w, h = detection[:4].int().tolist()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Tiny Face Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

