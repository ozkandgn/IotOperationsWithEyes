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

def enlighten_image(img,y,c):
	new_img = np.array(img)
	new_img = c * new_img**y
	new_img = normalization(new_img,255)
	return new_img.astype(np.uint8)

def mean_filter(img):
    filt = np.ones((5,5))/20
    return conv(img,filt)

def sobel_y(img):
    filt = np.array([[1,1,1], [0,0,0], [-1,-1,-1]])
    return conv(img,filt)

def black_and_white(img):
    avg = np.average(img)
    print("avg ",avg)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i,j] == avg:
                img[i,j] = 1
            else:
                img[i,j] = 0
    return img * 255

def image_operations(img,image_x,image_y):
    #img = image_filters.focus_filter(img,0.5,2)   
    #img = image_filters.sobel_y(img)
    img=cv2.resize(img,(image_x,image_y))
    img = enlighten_image(img,0.8,2)
    return mean_filter(img)