#
# The detector for flashing button by using color filter
# Created by haodong liu
#
import cv2
import numpy as np
from matplotlib import pyplot as plt
import util
import feature_detetor


confidence_counter = 0
org_pos_x = 0;
org_pos_y = 0;
org_size = 0;


def orange_flash_num(candidate):
    counter = 0
    for item1 in candidate:
        x1, y1, w1, h1 = cv2.boundingRect(item1)
        if (x1 < org_pos_x + 100 and x1 > org_pos_x - 100):
            if(y1 < org_pos_y + 100 and y1 > org_pos_y - 100):
                counter += 1
    return counter


def left_top_flash_num():

    return 0


def estimate_org_flash_size(area,org_size):
    half_size = org_size / 2
    left = half_size - org_size / 3
    right = org_size
    if area > left and area < right:
        return True
    return False


def reset():
    global confidence_counter
    confidence_counter = 0


def flash_detection(img1, img2, orange_x, orange_y, size,show_type = 0):

    print "---------------------------flash detection start"
    global org_pos_x;
    global org_pos_y;
    global confidence_counter;

    org_pos_x = orange_x
    org_pos_y = orange_y
    print org_pos_x,org_pos_y


    ret, thresh1 = cv2.threshold(img1, 205, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(img2, 205, 255, cv2.THRESH_BINARY)

    hsv1 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    hsv2 = cv2.cvtColor(thresh2, cv2.COLOR_BGR2GRAY)

    cnts1, hierarchy1 = cv2.findContours(hsv1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts2, hierarchy2 = cv2.findContours(hsv2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #cnts1 = cv2.findContours(hsv1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #cnts2 = cv2.findContours(hsv2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if show_type == 1:
        util.show_two_image(hsv1,hsv2)
    elif show_type == 2:
        util.show_image("w1",hsv1,640,320)
        util.show_image("w2",img2,640,320)

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

    print "for area of cnts 2"
    for cnt in cnts2:
        #if area0 > 10:
         #   print area0
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, False)
        #if area0 > 100:
            #print "area "+str(area0)
        if estimate_org_flash_size(area0,size):#feature_detetor.estimate_orange_area(area0,size):
            x, y, w, h = cv2.boundingRect(cnt)
            print org_pos_x,org_pos_y,x,y,area0
            org_btn_candidate_2.append(cnt)
    #counter1 = orange_flash_num(org_btn_candidate_1)
    counter2 = orange_flash_num(org_btn_candidate_2)

    if counter2 == 1:
        #print org_btn_candidate_2
        confidence_counter += 1
    if confidence_counter >= 4:
        print "detected"
        reset()
        cv2.imwrite("state3-1.jpg",img2)
        cv2.imwrite("state3-2.jpg",hsv2)
        return True
    print '------------end'
    return False