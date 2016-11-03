import util
import cv2

im1 = cv2.imread("../test1.jpg")
im2 = cv2.imread("../test2.jpg")
util.show_two_image(im1, im2)

ret, thresh1 = cv2.threshold(im1, 200, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(im2, 200, 255, cv2.THRESH_BINARY)

hsv1 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
hsv2 = cv2.cvtColor(thresh2, cv2.COLOR_BGR2GRAY)

util.show_two_image(hsv1,hsv2)

_, cnts1, hierarchy1 = cv2.findContours(hsv1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
_, cnts2, hierarchy2 = cv2.findContours(hsv2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print sum(cnts1)
print cnts2
