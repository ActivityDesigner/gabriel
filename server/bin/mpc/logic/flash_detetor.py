#
# The detector for flashing button by using color filter
# Created by haodong liu
#
import cv2
import numpy as np
from matplotlib import pyplot as plt
import util
import feature_detetor
import log
import color_filter
import const

confidence_counter = 0
org_pos_x = 0;
org_pos_y = 0;
org_size = 0;

TAG = "flash_detetor"

current_image = None
filter_image = None

def get_two_image():
    return current_image,filter_image


def orange_flash_num(candidate):
    counter = 0
    for item1 in candidate:
        x1, y1, w1, h1 = cv2.boundingRect(item1)
        if (x1 < org_pos_x + const.Dummy_Org_Flashing_Range and x1 > org_pos_x - const.Dummy_Org_Flashing_Range):
            if (y1 < org_pos_y + const.Dummy_Org_Flashing_Range and y1 > org_pos_y - const.Dummy_Org_Flashing_Range):
                counter += 1
    return counter


def left_top_flash_num():
    return 0


def estimate_org_flash_size(area, org_size):
    half_size = org_size / 2
    #left = org_size-const.Dummy_Org_Flashing_Size_Low #half_size - org_size / 3
    #right = org_size+const.Dummy_Org_Flashing_Size_Up #org_size
    left = half_size
    right = org_size
    if area > left and area < right:
        return True
    return False


def reset():
    global confidence_counter
    confidence_counter = 0


def flash_detection(img1, img2, orange_x, orange_y, size, show_type=0):

    log.print_debug(TAG,"----------flash detection start----------")
    global org_pos_x;
    global org_pos_y;
    global confidence_counter;
    global current_image
    global filter_image

    org_pos_x = orange_x
    org_pos_y = orange_y
    log.print_debug(TAG, "passed in org_pos_x "+str(org_pos_x)+" org_pos_y "+str(org_pos_y)+" size "+str(size))

    hsv1,hsv2 = color_filter.filter_flash(img1,img2)

    return1= cv2.findContours(hsv1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return2 = cv2.findContours(hsv2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cnts1 = cv2.findContours(hsv1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cnts2 = cv2.findContours(hsv2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    current_image = img2
    filter_image = hsv2

    if len(return1) == 3:
        cnts1 = return1[1]
        hierarchy1 = return1[2]
    else:
        cnts1 = return1[0]
        hierarchy1 = return1[1]

    if len(return2) == 3:
        cnts2 = return2[1]
        hierarchy2 = return2[2]
    else:
        cnts2 = return2[0]
        hierarchy2 = return2[1]

    if show_type == 1:
        util.show_two_image(hsv1, hsv2)
    elif show_type == 2:
        util.show_image("w1", hsv1, 640, 320)
        util.show_image("w2", img2, 640, 320)

    # org_btn_candidate_1 = []
    org_btn_candidate_2 = []

    # print "for area of cnts 1"
    # for cnt in cnts1:
    #     area0 = cv2.contourArea(cnt)
    #     #if area0 > 10:
    #     #    print area0
    #     cnt_len = cv2.arcLength(cnt, True)
    #     cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, False)
    #     #if area0 > 100:
    #         #print "area " + str(area0)
    #     if estimate_org_flash_size(area0, size):#feature_detetor.estimate_orange_area(area0,size):
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         print org_pos_x,org_pos_y,x,y,area0
    #         org_btn_candidate_1.append(cnt)

    log.print_debug(TAG, "for area of cnts 2")
    for cnt in cnts2:
        # if area0 > 10:
        #   print area0
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, False)
        if area0 > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            print "flash button area size " + str(area0) + " Posx " + str(x) + " Posy " + str(y)

        if estimate_org_flash_size(area0, size):  # feature_detetor.estimate_orange_area(area0,size):
            x, y, w, h = cv2.boundingRect(cnt)
            log.print_debug(TAG,"flash button area size "+str(area0)+" Posx " +str(x)+" Posy "+str(y))
            org_btn_candidate_2.append(cnt)
    # counter1 = orange_flash_num(org_btn_candidate_1)
    counter2 = orange_flash_num(org_btn_candidate_2)

    if counter2 >= 1:
        # print org_btn_candidate_2
        confidence_counter += 1
    if confidence_counter >= 4:
        log.print_debug(TAG, "detected!!")
        reset()
        return True
    print '------------end'
    return False
