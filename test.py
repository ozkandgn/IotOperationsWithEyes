from Image_Processing import image_filters
import cv2

img = cv2.imread("Image_Processing/train3/1loo12.png",0)
img = cv2.resize(img,(90,40))
cv2.imshow("f",img)

light_img = image_filters.gamma_correction(img,2.7)

cv2.imshow("l",light_img)

new_img = image_filters.black_and_white(light_img)
new_img2 = image_filters.black_and_white(img)

cv2.imshow("i",new_img)
cv2.imshow("i2",new_img2)

cv2.waitKey(0)