"""
Eye Tracking Module
Author: Hasan Baig
Date: January 16 2022
"""

import cv2
import mediapipe as mp

class EyeDetector:
    """
    Eye Detector identifies 32 Landmarks of left eye and right eye using the mediapipe library.
    Acquire the landmark points for the entire face (total of 468 landmarks)
    """

    def __init__(self, staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5):
        """
        :param staticMode: In static mode, detection is done on each image: slower
        :param maxFaces: Maximum number of faces to detect
        :param minDetectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode,
                                                 max_num_faces=self.maxFaces,
                                                 min_detection_confidence=self.minDetectionCon,
                                                 min_tracking_confidence=self.minTrackCon)

        # https://github.com/google/mediapipe/tree/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
        self.leftEye = [130, 25, 110, 24, 23, 22, 26, 112, 243, 190, 56, 28, 27, 29, 30, 247]               # landmarks labels of left eye
        self.rightEye = [359, 255, 339, 254, 253, 252, 256, 341, 463, 414, 286, 258, 257, 259, 260, 467]    # landmarks labels of right eye

    def findFaceMesh(self, img):
        """
        Finds face landmarks in BGR Image.
        :param img: Image to find the face landmarks in.
        :return: Image with or without drawings
        """
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    face.append([x, y])
                faces.append(face)
        return img, faces

    def drawEyeContour(self, img, face, draw=True):
        """
        Draws contour over eye landmarks in BGR Image.
        :param img: Image for draw the eye landmarks in.
        :param face: List of landmarks for the face in that frame.
        :param draw: Flag to draw the output on the image.
        """
        if draw:
            # Draw lines over left eye
            for index, left in enumerate(self.leftEye):
                if index != 0:
                    cv2.line(img, face[left], face[self.leftEye[index - 1]], (0, 255, 0), 2)
                else:
                    cv2.line(img, face[left], face[self.leftEye[15]], (0, 255, 0), 2)

            # Draw lines over right eye
            for index, right in enumerate(self.rightEye):
                if index != 0:
                    cv2.line(img, face[right], face[self.rightEye[index - 1]], (0, 255, 0), 2)
                else:
                    cv2.line(img, face[right], face[self.rightEye[15]], (0, 255, 0), 2)


def main():
    cap = cv2.VideoCapture(0)
    detector = EyeDetector(maxFaces=1)

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img)
        if faces:
            face = faces[0]
            detector.drawEyeContour(img, face)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()