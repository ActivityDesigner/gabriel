#
# The preparation for detecting the following three stages.
# Create by haodong liu
#
import cv2
import aed_detector
import util
import color_filter
import log
import const

TAG = "stage_pre_main"

#Const estimated size of orange button
Dummy_Org_Size_Min = const.Dummy_Org_Size_Min
Dummy_Org_Size_Max = const.Dummy_Org_Size_Max
Dummy_Similar_Dis = const.Dummy_Similar_Dis
Confidence_Min_Counter = const.Dummy_Confidence_Min_Counter

current_image = None
filter_image = None
contour_image = None

# orange button
detected_org_x = 0
detected_org_y = 0
detected_org_size = 0
detected_counter = 0

def reset():
    global detected_counter
    detected_counter = 0


#
# For retrieving the detected orange button params
#
def retrieve_org_btn_params():
    return detected_org_x,detected_org_y,detected_org_size


def get_two_image():
    return current_image,filter_image


def get_contour_image():
    return None


def within_org_dummy_size(size):

    if size < Dummy_Org_Size_Max and size > Dummy_Org_Size_Min:
        return True
    return False


def is_similar(cnts1,cnts2):

    global contour_image

    to_return = []
    min_dis = Dummy_Similar_Dis
    for cnt1 in cnts1:
        for cnt2 in cnts2:
            x1, y1, w1, h1 = cv2.boundingRect(cnt1)
            x2, y2, w2, h2 = cv2.boundingRect(cnt2)
            dis = abs(x1 - x2) + abs(y1 - y2)
            if dis < min_dis:
                min_dis = dis
                area0 = cv2.contourArea(cnt2)
                to_return = [x2,y2,area0]
                #
                #contour_image =
    return to_return


def prepare(last_valid_frame,frame):

    log.print_debug(TAG,"------------prepare------------")

    is_prepared = False
    global detected_org_x
    global detected_org_y
    global detected_org_size
    global detected_counter
    global current_image
    global filter_image

    res1, res2 = color_filter.filter_orange(last_valid_frame, frame)
    # transfer HSV to Binary image for contour detection
    tmp1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
    tmp2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
    black1 = cv2.cvtColor(tmp1, cv2.COLOR_BGR2GRAY)
    black2 = cv2.cvtColor(tmp2, cv2.COLOR_BGR2GRAY)
    ret1, thresh1 = cv2.threshold(black1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(black2, 0, 255, cv2.THRESH_BINARY)
    return1 = cv2.findContours(thresh1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return2 = cv2.findContours(thresh2.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    current_image = frame
    filter_image = res2

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

    # cnts1 and cnts2 contain the contour result
    org_btn_candidate_1 = []
    org_btn_candidate_2 = []

    log.print_debug(TAG,"image1 begin find")
    for cnt in cnts1:
        area0 = cv2.contourArea(cnt)
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if area0 > 100:
            x1, y1, w1, h1 = cv2.boundingRect(cnt)
            log.print_debug(TAG, "orange button area size > 100 "+str(area0)+" Posx "+str(x1) +" Posy "+str(y1))
        if within_org_dummy_size(area0):
            x1, y1, w1, h1 = cv2.boundingRect(cnt)
            log.print_debug(TAG, "orange button candidate area size "+str(area0)+" Posx "+str(x1) +" Posy "+str(y1))
            org_btn_candidate_1.append(cnt)
    log.print_debug(TAG,"image1 end find")

    log.print_debug(TAG,"image2 begin find")
    for cnt in cnts2:
        cnt_len = cv2.arcLength(cnt, True)
        area0 = cv2.contourArea(cnt)
        cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        if within_org_dummy_size(area0):
            x1, y1, w1, h1 = cv2.boundingRect(cnt)
            log.print_debug(TAG, "orange button candidate area size "+str(area0)+" Posx "+str(x1) +" Posy "+str(y1))
            org_btn_candidate_2.append(cnt)
    log.print_debug(TAG,"image2 end find")

    nums = is_similar(org_btn_candidate_1,org_btn_candidate_2)
    if len(nums) > 0:
        detected_counter += 1
        if detected_counter > Confidence_Min_Counter:
            reset()
            is_prepared = True
            detected_org_x = nums[0]
            detected_org_y = nums[1]
            detected_org_size = nums[2]
            log.print_debug(TAG,"find orange button area size " + str(nums[2]) + " Posx " + str(nums[0]) + " Posy " + str(nums[1]))
    # is_aed_detected = aed_detector.aed_detect(last_valid_frame, frame)
    # # now find the orange button and other important items precisely
    # if is_aed_detected:
    #     # get the orange button position and relative size
    #     a = 0
    # else:
    #     is_prepared = False
    return is_prepared
