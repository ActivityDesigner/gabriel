#
# The self-convenience util tools
# Created by haodong liu
#
import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_resized_img(img):
    screen_res = 1000, 500
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    print window_width,window_height
    cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('dst_rt', window_width, window_height)
    cv2.imshow('dst_rt', img)

def show_two_image(image1,image2):
    img_two = np.concatenate((image1, image2), axis=1)
    plt.imshow(img_two)
    plt.show()


def show_image(name,image,x = 640,y = 320):
    dim = (x,y)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(name,resized)


def getRotatedImage(image_file, green_loc, yellow_loc, blue_loc):
    '''
    :param image_file: file name
    :param green_loc: list[x, y]
    :param yellow_loc: list[x, y]
    :param blue_loc:  list[x, y]
    :return: rotated image
    '''
    img = cv2.imread(image_file)
    rows,cols,ch = img.shape
    pts1 = np.float32([[687, 205], [278, 418], [767, 384]])
    pts2 = np.float32([green_loc, yellow_loc, blue_loc])
    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst


def debug_print(tag,msg,is_show = True):
    if is_show:
        print tag +" " + str(msg)