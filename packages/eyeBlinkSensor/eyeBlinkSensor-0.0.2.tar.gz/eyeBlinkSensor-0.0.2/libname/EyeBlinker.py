"""
Eye Blink Sensor Project
By: Rischit Aggarwal
"""

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


capture = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)


def EyeBlinker():
    """
    Eye Blinker counts the number of times you blink your eye
    :param None
    """

    plotY = LivePlot(640, 360, [20, 50])

    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
    ratioList = []
    blinkCounter = 0
    counter = 0
    color = (255, 0, 255)


    while True:

        if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, image = capture.read()
        image, faces = detector.findFaceMesh(image, draw=False)

        if faces:
            face = faces[0]
            """
            If you want to draw the circle to determine the ratio, please comment out the line given below
            """
            # for id in idList:
            #     cv2.circle(image, face[id], 5, color, cv2.FILLED)

            leftEye_upPart = face[159]
            leftEye_downPart = face[23]
            leftEye_leftPart = face[130]
            leftEye_rightPart = face[243]
            length_Vertical, _ = detector.findDistance(leftEye_upPart, leftEye_downPart)
            length_Horizontal, _ = detector.findDistance(leftEye_leftPart, leftEye_rightPart)

            """
            If you want to draw the lines to determine the ratio, please comment out the line given below
            """

            # cv2.line(image, leftEye_upPart, leftEye_downPart, (0, 200, 0), 3)
            # cv2.line(image, leftEye_leftPart, leftEye_rightPart, (0, 200, 0), 3)

            ratio = int((length_Vertical / length_Horizontal) * 100)
            ratioList.append(ratio)
            if len(ratioList) > 3:
                ratioList.pop(0)
            ratioAvg = sum(ratioList) / len(ratioList)

            if ratioAvg < 35 and counter == 0:
                blinkCounter += 1
                color = (0, 200, 0)
                counter = 1
            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
                    color = (255, 0, 255)

            cvzone.putTextRect(image, f'Blink Count: {blinkCounter}', (50, 100),
                               colorR=color)

            imagePlot = plotY.update(ratioAvg, color)
            image = cv2.resize(image, (640, 360))
            imageStack = cvzone.stackImages([image, imagePlot], 2, 1)
        else:
            image = cv2.resize(image, (640, 360))
            imageStack = cvzone.stackImages([image, image], 2, 1)

            
        cv2.imshow("EyeBlink Sensor", imageStack)
        cv2.waitKey(25)

if __name__ == "__main__":
    EyeBlinker()