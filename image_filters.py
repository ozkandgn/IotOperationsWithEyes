import numpy as np
import cv2

def normalization(val,max_val):
    min_v = np.min(val)
    max_v = np.max(val)
    return ((val-min_v))/(max_v-min_v)*max_val

def conv(img,filt):
    return cv2.filter2D(img, -1, filt)

def focus_filter(img,y,c):
    new_img = np.array(img)
    new_img = c * new_img**y
    filt = np.array([[-1,-2,-1], [-2,0,-2], [-1,-2,-1]])
    new_img = conv(new_img,filt)
    new_img = normalization(new_img,255)
    return new_img.astype(np.uint8)

def sobel_y(img):
    filt = np.array([[1,1,1], [0,0,0], [-1,-1,-1]])
    return conv(img,filt)