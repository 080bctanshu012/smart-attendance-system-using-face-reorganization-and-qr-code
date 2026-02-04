#!/usr/bin/env python3
"""
Test script to diagnose face recognition with real camera
"""

import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

print("Testing face recognition with camera...")
print("="*50)

# Capture an image from camera
print("\n1. Capturing image from camera...")
camera = cv2.VideoCapture(0)
success, frame = camera.read()
camera.release()

if not success:
    print("   ERROR: Could not capture image from camera!")
else:
    print(f"   Image captured successfully! Shape: {frame.shape}")
    
    # Save the captured image
    test_dir = 'static/images/faces'
    os.makedirs(test_dir, exist_ok=True)
    test_image_path = os.path.join(test_dir, 'test_capture.jpg')
    cv2.imwrite(test_image_path, frame)
    print(f"   Image saved to: {test_image_path}")

    # Convert to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Try to detect faces
    print("\n2. Detecting faces...")
    face_locations = face_recognition.face_locations(rgb_frame)
    print(f"   Found {len(face_locations)} face(s)")
    
    if face_locations:
        print("   Face locations (top, right, bottom, left):")
        for i, loc in enumerate(face_locations):
            print(f"   Face {i+1}: {loc}")
        
        # Try to get face encodings
        print("\n3. Generating face encodings...")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print(f"   Generated {len(face_encodings)} encoding(s)")
        
        if face_encodings:
            print(f"   Encoding shape: {face_encodings[0].shape}")
            print(f"   First few values: {face_encodings[0][:5]}")
            print("\n   SUCCESS: Face encoding generated!")
    else:
        print("\n   WARNING: No faces detected!")
        print("\n   Tips for better face detection:")
        print("   - Ensure good lighting (avoid shadows)")
        print("   - Face the camera directly")
        print("   - Stay about 1-2 meters from camera")
        print("   - Remove glasses or hats if possible")
        print("   - Keep a neutral expression")
        print("   - Ensure only one face in frame")

print("\n" + "="*50)
print("Test complete!")
