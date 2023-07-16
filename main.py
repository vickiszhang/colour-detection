import cv2
import numpy as np
import time
import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def empty():
    pass

width = 532 #round(screen_width / 2)
height = 400 #round(screen_height / 2)
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.namedWindow("Colour Picker", cv2.WINDOW_NORMAL)

cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

video_capture = cv2.VideoCapture(0)


if not video_capture.isOpened():
    print("Failed to open the camera")

def process_frame(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    img_result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return imgHSV, mask, img_result

while (video_capture.isOpened()):
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_HSV, mask, img_result = process_frame(frame)

    frame = cv2.resize(frame, (width, height))
    img_HSV = cv2.resize(img_HSV, (width, height))
    mask = cv2.resize(mask, (width, height))
    img_result = cv2.resize(img_result, (width, height))

    # cv2.imshow("Original", frame)
    # cv2.imshow('HSV', img_HSV)
    # cv2.imshow('Mask', mask)
    # cv2.imshow("Colour", img_result)

    top_row = np.concatenate((frame, img_HSV), axis=1)
    bottom_row = np.concatenate((mask, img_result), axis=1)
    composite_image = np.concatenate((top_row, bottom_row), axis=0)

    cv2.imshow("Colour Picker", composite_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



video_capture.release()
cv2.destroyAllWindows()