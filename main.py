import cv2

frameWidth = 640
frameHeight = 480

video_capture = cv2.VideoCapture(0)

detect_colours = []
if not video_capture.isOpened():
    print("Failed to open the camera")

def find_colour(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BAYER_BGR2HSV)

while (video_capture.isOpened()):
    ret, frame = video_capture.read()
    if not ret:
        break

    flipped_frame = cv2.flip(frame, 1)
    cv2.imshow('Video', flipped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()