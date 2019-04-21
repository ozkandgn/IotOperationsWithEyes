import cv2
from cnn import Detect
from take_photo import SaveEye
from create_and_detect import Detector
from region import Region

from blinking_counter import Blinking

count=0

regions = Region()
save_eye = SaveEye()
detectors = Detector()
blinking_right = Blinking()
blinking_left = Blinking()
set_blink_right = blinking_right.set_blink
set_blink_left = blinking_left.set_blink
key=0

rasp = True

class Eye():
    def __init__(self):
        if rasp:
            from get_image_rasp import CapImage
            from picamera import PiCamera
            cap = PiCamera() 
            #cap.color_effects = (128,128)
            cap.start_preview()
            c_i = CapImage(cap)
            self.read_frame = c_i.get_image
            
        else:
            cap = cv2.VideoCapture(0)
            self.read_frame = cap.read
            
        self.det = Detect()
        
    def get_eye_frame(self):
        _, frame = self.read_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detectors.create(gray)  
        for face in faces:
            
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x1, y1), (80,127,255), 2)
            
            right_gray_eye = regions.create(gray,frame,face,[36,37,38,39,40,41])
            left_gray_eye = regions.create(gray,frame,face,[42,43,44,45,46,47])

            try:
                right_eye = cv2.resize(right_gray_eye, None, fx=5, fy=5)
                left_eye = cv2.resize(left_gray_eye, None, fx=5, fy=5)
                right_eye_result = float(self.det.set_img(right_eye))
                left_eye_result = float(self.det.set_img(left_eye))

            except:
                print("hataaaa")
                right_eye_result = -1
                left_eye_result = -1
                pass
            
            #cv2.imshow("Right Eye", right_eye)
            #cv2.imshow("Left Eye", left_eye)
            #print("Right eye=",right_eye_result)
            #print("Left eye=",left_eye_result)
            key = cv2.waitKey(1)
            if key == 49: # save photo press 1
                save_eye.take_photo(left_gray_eye,"train_rasp/1loo1")
            if key == 50: # save photo press 2
                save_eye.take_photo(left_gray_eye,"train_rasp/2lcc1")
            if key == 51: # save photo press 3
                save_eye.take_photo(right_gray_eye,"train_rasp/1roo1")
            if key == 52: # save photo press 4
                save_eye.take_photo(right_gray_eye,"train_rasp/2rcc1")
        
            cv2.imshow("Frame", frame)
            return (right_eye_result,left_eye_result)
'''
eye_test = Eye()
while True:
    eye_test.get_frame()
'''