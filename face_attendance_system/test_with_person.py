#!/usr/bin/env python3
"""
Test script - RUN THIS WITH YOUR FACE IN FRONT OF CAMERA
"""

import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

print("Face Recognition Test")
print("="*50)
print("Please position your face in front of the camera...")
print("The test will run for 5 seconds and try to detect your face.")
print("="*50)

camera = cv2.VideoCapture(0)
start_time = cv2.getTickCount()

while True:
    success, frame = camera.read()
    if not success:
        break
    
    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    
    # Draw rectangle around faces
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    
    # Show frame
    cv2.imshow('Face Detection Test', frame)
    
    # Print status
    elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    if int(elapsed) % 1 == 0:  # Print every second
        print(f"Time: {elapsed:.1f}s - Found {len(face_locations)} face(s)")
    
    # Exit after 5 seconds or on key press
    if elapsed > 5 or cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

print("\n" + "="*50)
if face_locations:
    print("SUCCESS: Face detection is working!")
    print(f"Detected {len(face_locations)} face(s)")
else:
    print("FAILURE: No faces detected!")
    print("\nPossible issues:")
    print("1. Lighting too dark or too bright")
    print("2. Face not facing camera directly")
    print("3. Face too far or too close")
    print("4. Library compatibility issue")
    print("\nTry the following:")
    print("- Move closer to camera (about 1 meter)")
    print("- Improve room lighting")
    print("- Face camera directly")
    print("- Remove glasses/hat if wearing")
print("="*50)
