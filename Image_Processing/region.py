import cv2
from .create_and_detect import Landmark
import numpy as np

class Region():
    def __init__(self):
        self.landmarks = Landmark()
    def create(self,gray,frame,face,points):
        right_eye_region = self.landmarks.create(gray,face,points)
        
        cv2.polylines(frame, [right_eye_region], True, (0, 255, 0), 1)
     
        height, width, _ = frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [right_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [right_eye_region], 255)
        right_eye = cv2.bitwise_and(gray, gray, mask=mask)
     
        min_x = np.min(right_eye_region[:, 0])
        max_x = np.max(right_eye_region[:, 0])
        min_y = np.min(right_eye_region[:, 1])
        max_y = np.max(right_eye_region[:, 1])
     
        return right_eye[min_y: max_y, min_x: max_x]