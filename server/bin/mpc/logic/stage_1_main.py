#
# Used for detecting stage one, namely to see if AED has been turned on
# Created by haodong liu
#
import flash_detetor
import feature_detetor
import util
import stage_pre_main

TAG = "stage_1_main"
Failed_Tolerant = 30

org_size = 0
detected_x = 0
detected_y = 0
failed_counter = 0
success_counter = 0
is_detected = False


# Setting params for orange button
def set_org_params(x, y, size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org


# Retrieving orange button params
def retrieve_org_params():
    return detected_x, detected_y, org_size


# 1.detect the range of start btn
# 2.detect hand appearing in the range of start btn
# 3.detect flashing orange button in the next three frames, if happend, return true,
is_hand_appearing = False
hand_disappear_cnt = 0


def run(last_valid_frame, frame):
    # start_btn_x,start_btn_y = feature_detetor.detect_start_btn(last_valid_frame,frame)

    # hand_x,hand_y = feature_detetor.detect_hand(last_valid_frame,frame)

    # print hand_x, hand_y

    global is_hand_appearing;
    global hand_disappear_cnt;
    global detected_x
    global detected_y
    global org_size
    global failed_counter
    global success_counter
    is_hand_appearing = True

    # if abs(hand_x - start_btn_x) < 200 and abs(hand_y - start_btn_y) < 200:
    #     # the hand is right above the btn
    #     is_hand_appearing = True
    #     hand_disappear_cnt = 0
    # else:
    #     hand_disappear_cnt += 1
    #     if hand_disappear_cnt > 5:
    #         is_hand_appearing = False
    is_flash_detected = False

    # dynamically update the orange button location, pass it into the flash detection
    x, y, size, is_success = feature_detetor.detect_orange_btn(last_valid_frame, frame, detected_x, detected_y,
                                                               org_size, 0)
    detected_x = x
    detected_y = y
    org_size = size

    # if we detect the aed device is not within the screen or orange button is missing for
    if is_success == False:
        # using a tolerate false detection range
        util.debug_print(TAG, "fail to find orange button")
        failed_counter += 1
        if failed_counter > Failed_Tolerant:
            # the aed device is missing, start the refind process
            util.debug_print(TAG, "The AED device is missing, preparation again")
            is_find = stage_pre_main.prepare(last_valid_frame, frame)
            if is_find:
                failed_counter = 0
                detected_x, detected_y, org_size = stage_pre_main.retrieve_org_btn_params()

    if is_hand_appearing:
        is_detect = flash_detetor.flash_detection(last_valid_frame, frame, detected_x, detected_y, org_size, 0)
        if is_detect:
            return True
    return False
