import cv2
import numpy as np

class DrawTool:
    
    width = 732
    height = 550 
    join_frames = True
    colours = {"red": [0, 179, 157, 255, 0, 255], 
               "blue": [88, 101, 48, 255, 32, 144], 
               "green": [37, 67, 44, 127, 68, 177], 
               "purple": [127, 152, 56, 130, 29, 195]
    }
    colours_bgr = {"red": [0, 0, 255],   
                   "blue": [255, 0, 0], 
                   "green": [0, 255, 0], 
                   "purple": [266, 43, 138],
    }
    points = []
    
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

            img_drawing = original.copy()
            contours_img = original.copy()
            new_points = self.find_colour(original, contours_img)

            if len(new_points) != 0:
                for np in new_points:
                    self.points.append(np)
            if len(self.points) != 0:
                self.draw_points(img_drawing)

            if self.join_frames:
                composite_frame = self.combine_frames(img_drawing, contours_img)
                cv2.imshow("Drawing", composite_frame)
            else:
                cv2.imshow("Result", img_drawing)
                cv2.imshow("Contours", contours_img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

    def find_colour(self, img, contours_img):
        new_points = []
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  

        for key, value in self.colours.items():
            lower = np.array(value[0::2])
            upper = np.array(value[1::2])
            mask = cv2.inRange(img_HSV, lower, upper)
            x, y = self.get_contours(mask, contours_img, colour=key)
            if x != 0  and y != 0:
                new_points.append([x, y, key])
            cv2.circle(contours_img, (x,y), 8, (255, 255, 255), cv2.FILLED)

        return new_points

    
    def get_contours(self, img, contours_img, colour):
        x, y, w, h = 0, 0, 0, 0
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                cv2.drawContours(contours_img, cnt, -1, self.colours_bgr[colour], 2)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)

        return x + w // 2, y
    
    def draw_points(self, img_drawing):
        for point in self.points:
            cv2.circle(img_drawing, (point[0], point[1]), 8, self.colours_bgr[point[2]], cv2.FILLED)

    def combine_frames(self, img_drawing, contours_img):
            img_drawing = cv2.resize(img_drawing, (self.width, self.height))
            contours_img = cv2.resize(contours_img, (self.width, self.height))

            row = np.concatenate((img_drawing, contours_img), axis=1)
            composite_image = row

            return composite_image
