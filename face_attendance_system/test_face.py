#!/usr/bin/env python3
"""
Test script to diagnose face recognition issues
"""

import cv2
import face_recognition
import numpy as np
import os

print("Testing face recognition setup...")

# Test 1: Check if libraries are imported correctly
print("\n1. Library imports:")
print(f"   OpenCV version: {cv2.__version__}")
print(f"   face_recognition version: {face_recognition.__version__}")

# Test 2: Check camera
print("\n2. Camera test:")
camera = cv2.VideoCapture(0)
if camera.isOpened():
    success, frame = camera.read()
    if success:
        print("   Camera is working!")
        print(f"   Frame size: {frame.shape}")
    else:
        print("   Camera read failed!")
else:
    print("   Camera could not be opened!")
camera.release()

# Test 3: Check face detection in a test image
print("\n3. Face detection test:")
# Create a simple test image with a white background
test_image = 255 * np.ones((480, 640, 3), dtype=np.uint8)
rgb_frame = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

# Try to detect faces
face_locations = face_recognition.face_locations(rgb_frame)
print(f"   Face locations in blank image: {face_locations}")

# Test 4: Check if models are loaded
print("\n4. Checking face recognition models...")
try:
    # Try to load a dummy image to check model
    import numpy as np
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    encodings = face_recognition.face_encodings(test_img)
    print(f"   Face encoding on blank image: {len(encodings)} faces detected")
except Exception as e:
    print(f"   Error: {e}")

# Test 5: Check static folder
print("\n5. Checking static folder...")
upload_folder = 'static/images/faces'
if os.path.exists(upload_folder):
    files = os.listdir(upload_folder)
    print(f"   Files in upload folder: {files}")
else:
    print(f"   Upload folder does not exist: {upload_folder}")

print("\n" + "="*50)
print("If face detection fails, try:")
print("1. Better lighting conditions")
print("2. Face the camera directly")
print("3. Remove glasses or hats")
print("4. Ensure only one face in frame")
print("="*50)
