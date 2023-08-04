import cv2
import numpy as np

class DrawTool:

    colours = {"red": [0, 179, 157, 255, 0, 255], 
               "blue": [88, 101, 48, 255, 32, 144], 
               "green": [37, 67, 44, 127, 68, 177], 
    }

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)

    def run(self):
        if not self.video_capture.isOpened():
            print("Failed to open the camera")

        while (self.video_capture.isOpened()):
            ret, frame = self.video_capture.read()
            if not ret:
                break
            original = cv2.flip(frame, 1)

            cv2.imshow("Result", original)
            self.find_colour(original)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

    def find_colour(self, img):
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for key, value in self.colours.items():
            lower = np.array(value[0::2])
            upper = np.array(value[1::2])
            mask = cv2.inRange(img_HSV, lower, upper)
            cv2.imshow(key, mask)