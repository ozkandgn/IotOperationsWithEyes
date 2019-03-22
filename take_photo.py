import cv2

class SaveEye():
    def __init__(self):
        self.count = 0
        
    def take_photo(self,img,text): #cv2 save photo
        cv2.imwrite(str(text)+'{}.png'.format(self.count),img)#img should be gray
        self.count+=1
        print("success")