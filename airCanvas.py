"""
AirCanvas: Real-time air drawing using MediaPipe and OpenCV.
Tracks index and thumb fingers to simulate a stylus.
"""

import cv2
import mediapipe as mp
import numpy as np
import math

# 1. Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# 2. Initialize Webcam and Canvas
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Width
cap.set(4, 720)  # Height

# Separate canvas to prevent the drawing from clearing every frame
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# 3. State Variables
current_color = (255, 0, 0) # Default: Blue (BGR format)
brush_size = 8
px, py = 0, 0 # Previous X and Y coordinates

while True:
    success, frame = cap.read()
    if not success:
        break
    
    # Flip frame horizontally for a natural mirror-like drawing experience
    frame = cv2.flip(frame, 1)
    
    # UI: Draw color selection palettes at the top
    cv2.rectangle(frame, (20, 20), (120, 70), (255, 0, 0), cv2.FILLED) # Blue Box
    cv2.rectangle(frame, (140, 20), (240, 70), (0, 0, 255), cv2.FILLED) # Red Box
    cv2.putText(frame, "BLUE", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "RED", (165, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Convert to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract coordinates for Thumb (4) and Index (8)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Map normalized coordinates (0.0 to 1.0) to pixel dimensions
            h, w, c = frame.shape
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)

            # Color Selection Logic: If index finger is in the UI boxes
            if iy < 70:
                if 20 < ix < 120:
                    current_color = (255, 0, 0) # Blue
                elif 140 < ix < 240:
                    current_color = (0, 0, 255) # Red

            # Calculate distance between thumb and index 
            distance = math.hypot(tx - ix, ty - iy)

            # Pinch Detection (Threshold)
            if distance < 40: # Increase this threshold if drawing flickers
                # If it's the first frame of a new stroke, set previous points to current
                if px == 0 and py == 0:
                    px, py = ix, iy
                
                # Draw on the separate canvas
                cv2.line(canvas, (px, py), (ix, iy), current_color, brush_size)
                px, py = ix, iy # Update previous points
            else:
                # Release: Reset previous points so the next stroke doesn't connect
                px, py = 0, 0 

            # Optional: Draw hand skeleton for visual debugging
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 4. Merge Canvas and Webcam Frame
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    
    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("AirCanvas", frame)
    
    # Press 'q' or 'ESC' to quit
    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()