#
# A filter to extract target color of AED device.
# Created by haodong liu
#
import cv2
import numpy as np


def filter_flash(image1, image2):
    #ret, thresh1 = cv2.threshold(image1, 205, 255, cv2.THRESH_BINARY)
    #ret, thresh2 = cv2.threshold(image2, 205, 255, cv2.THRESH_BINARY)
    #floor
    ret, thresh1 = cv2.threshold(image1, 254, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(image2, 254, 255, cv2.THRESH_BINARY)
    #ret, thresh1 = cv2.threshold(image1, 254, 255, cv2.THRESH_BINARY)
    #ret, thresh2 = cv2.threshold(image2, 254, 255, cv2.THRESH_BINARY)

    hsv1 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    hsv2 = cv2.cvtColor(thresh2, cv2.COLOR_BGR2GRAY)
    return hsv1,hsv2


#
# transform two image using red-only filter
#
def filter_red(image1, image2):
    # loop over the contours
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([30, 135, 100])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1, res2


#
# transform two image using green-only filter
#
def filter_green(image1, image2):
    # loop over the contours
    lower_green = np.array([100, 20, 20])
    upper_green = np.array([255, 100, 100])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_green, upper_green)
    mask2 = cv2.inRange(hsv2, lower_green, upper_green)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1, res2


#
# transform two image using orange-only filter
#
def filter_orange(image1, image2):
    # loop over the contours
    # the first
    #lower_blue = np.array([1, 120, 44]) #44
    #upper_blue = np.array([10, 255, 255])

    #qi
    #lower_blue = np.array([5, 0, 128])
    #upper_blue = np.array([40, 255, 255])

    #lower_blue = np.array([8, 100, 100])
    #upper_blue = np.array([16, 130, 255])

    lower_blue = np.array([8, 100, 100])
    upper_blue = np.array([16, 150, 255])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1, res2


def filter_yellow(image1, image2):

    lower_blue = np.array([20, 100, 100])
    upper_blue = np.array([35, 150, 255])
    #lower_blue = np.array([4, 135, 44])
    #upper_blue = np.array([43, 255, 255])
    # transfer to HSV image
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    # mask HSV image using low or upper blue
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    res1 = cv2.bitwise_and(image1.copy(), image1.copy(), mask=mask1)
    res2 = cv2.bitwise_and(image2.copy(), image2.copy(), mask=mask2)
    return res1, res2