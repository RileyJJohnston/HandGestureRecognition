"""
Computer Vision Integrated with Machine Learning
Author: Hasan Baig
Date: February 15 2022
"""

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from A_Computer_Vision.HandTrackingModule import HandDetector
from A_Computer_Vision.EyeTrackingModule import EyeDetector

MODEL_NAME = "mp_hand_gesture"

eyeDetector = EyeDetector(maxFaces=1)
handDetector = HandDetector(detectionCon=0.7, maxHands=1)

# Load the gesture recognizer model
model = load_model(MODEL_NAME)

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read each frame from the webcam
    _, frame = cap.read()
    className = ''

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)

    # Find the eyes and its landmarks with draw
    frame, eyes = eyeDetector.findFaceMesh(frame)

    # Find the hand and its landmarks with draw
    hands, frame = handDetector.findHands(frame)

    # If eyes are detected
    if eyes:
        # Draw contour around detected eyes
        eyeDetector.drawEyeContour(frame, eyes[0])

        # If hands are detected
        if hands:
            # Label hands
            hand1 = hands[0]
            if len(hands) == 2:
                hand2 = hands[1]

            # Predict gesture
            prediction = model.predict([hand1["lmList"]])
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()