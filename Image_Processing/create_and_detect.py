from dlib import shape_predictor,get_frontal_face_detector
import numpy as np

class Landmark():
    def __init__(self):
        self.predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")
        
    def create(self,gray,face,points):
        
        landmarks = self.predictor(gray, face)
             
        return np.array([(landmarks.part(points[0]).x, landmarks.part(points[0]).y),
                                    (landmarks.part(points[1]).x, landmarks.part(points[1]).y),
                                    (landmarks.part(points[2]).x, landmarks.part(points[2]).y),
                                    (landmarks.part(points[3]).x, landmarks.part(points[3]).y),
                                    (landmarks.part(points[4]).x, landmarks.part(points[4]).y),
                                    (landmarks.part(points[5]).x, landmarks.part(points[5]).y)], np.int32)
    
class Detector():
    def __init__(self):
        self.detector = get_frontal_face_detector()
        
    def create(self,gray):
        return self.detector(gray)