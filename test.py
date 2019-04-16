import image_filters,cv2

img = cv2.imread("train3/1loo12.png",0)

new_img = image_filters.black_and_white(img)

cv2.imshow("i",new_img)

cv2.waitKey(0)