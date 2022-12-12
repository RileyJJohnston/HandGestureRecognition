"""
Hand and Eye Tracking Module
Author: Hasan Baig
Date: January 16 2022
"""

import cv2
from HandTrackingModule import HandDetector
from EyeTrackingModule import EyeDetector

def main():
    cap = cv2.VideoCapture(0)
    eyeDetector = EyeDetector(maxFaces=1)
    handDetector = HandDetector(detectionCon=0.8, maxHands=2)

    while True:
        isHandsDetected = False
        isEyesDetected = False

        # Get image frame
        success, img = cap.read()

        # Flip the frame vertically
        img = cv2.flip(img, 1)

        # Find the face and its landmarks with draw
        img, faces = eyeDetector.findFaceMesh(img)

        # Find the hand and its landmarks with draw
        hands, img = handDetector.findHands(img)

        if faces:
            face = faces[0]
            eyeDetector.drawEyeContour(img, face)
            isEyesDetected = True

        if hands:
            isHandsDetected = True
            hand1 = hands[0]
            if len(hands) == 2:
                hand2 = hands[1]

        if isEyesDetected == True and isHandsDetected == False:
            print("eyes")
        elif isEyesDetected == False and isHandsDetected == True:
            print("hands")
        elif isEyesDetected == True and isHandsDetected == True:
            print("both")
        else:
            print("None")

        # Display
        cv2.imshow("Webcam", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()


