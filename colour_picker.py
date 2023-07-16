import cv2
import numpy as np
import time
import ctypes

class ColourPicker():

    width = 532
    height = 400 
    join_frames = True

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)

    def run(self):
        if not self.video_capture.isOpened():
            print("Failed to open the camera")
        self.create_windows()
        self.create_trackbars()

        while (self.video_capture.isOpened()):
            ret, frame = self.video_capture.read()
            if not ret:
                break
            
            original = cv2.flip(frame, 1)
            img_HSV, mask, colour_mask = self.process_frame(original)

            if self.join_frames:
                composite_frame = self.combine_frames(original, img_HSV, mask, colour_mask)
                cv2.imshow("Colour Picker", composite_frame)
            else:
                cv2.imshow("Original", original)
                cv2.imshow('HSV', img_HSV)
                cv2.imshow('Mask', mask)
                cv2.imshow("Colour", colour_mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.terminate()

    def create_windows(self):
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 640, 240)
        cv2.namedWindow("Colour Picker", cv2.WINDOW_NORMAL)
        
    def create_trackbars(self):
        cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, lambda x: None)
        cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, lambda x: None)
        cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, lambda x: None)
        cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, lambda x: None)
        cv2.createTrackbar("Val Min", "TrackBars", 0, 255, lambda x: None)
        cv2.createTrackbar("Val Max", "TrackBars", 255, 255, lambda x: None)

    def process_frame(self, original):
        img_HSV = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
        print(h_min, h_max, s_min, s_max, v_min, v_max)

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(img_HSV, lower, upper)

        colour_mask = cv2.bitwise_and(original, original, mask=mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        return img_HSV, mask, colour_mask

    def combine_frames(self, frame, img_HSV, mask, colour_mask):
            frame = cv2.resize(frame, (self.width, self.height))
            img_HSV = cv2.resize(img_HSV, (self.width, self.height))
            mask = cv2.resize(mask, (self.width, self.height))
            colour_mask = cv2.resize(colour_mask, (self.width, self.height))

            top_row = np.concatenate((frame, img_HSV), axis=1)
            bottom_row = np.concatenate((mask, colour_mask), axis=1)
            composite_image = np.concatenate((top_row, bottom_row), axis=0)

            return composite_image

    def terminate(self):
        video_capture.release()
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    colour_picker = ColourPicker()
    colour_picker.run()