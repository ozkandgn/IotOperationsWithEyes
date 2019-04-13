import cv2
from cnn import Detect
from take_photo import SaveEye
from create_and_detect import Detector
from region import Region

count=0

regions = Region()
save_eye = SaveEye()
detectors = Detector()
key=0
while True:
    cap = cv2.VideoCapture(0)
    det = Detect()
     
    font = cv2.FONT_HERSHEY_PLAIN
    
    while True:
        _, frame = cap.read()
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
            except:
                pass
            
            #cv2.imshow("Right Eye", right_eye)
            cv2.imshow("Left Eye", left_eye)
            print("Right eye=",det.set_img(right_eye))
            print("Left eye=",det.set_img(left_eye))
            key = cv2.waitKey(1) #1000 yap
            if key == 49: # save photo press 1
                save_eye.take_photo(left_gray_eye,"train3/1loo1")
            if key == 50: # save photo press 2
                save_eye.take_photo(left_gray_eye,"train3/2lcc1")
            if key == 51: # save photo press 3
                save_eye.take_photo(right_gray_eye,"train3/1roo1")
            if key == 52: # save photo press 4
                save_eye.take_photo(right_gray_eye,"train3/2rcc1")
        cv2.imshow("Frame", frame)
        if key == 98:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    if key == 98:
        break
    #return right_gray_eye
    
#img = cv2.imread("test/3.png",0)


