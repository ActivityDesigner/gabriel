#
# Used for detecting stage three, namely to see if orange button has been pressed
# Created by haodong liu
#
import flash_detetor
import feature_detetor

detected_x = 0
detected_y = 0
org_size = 0
is_flashing = False
no_flashing_cnt = 0
NO_FLASHING_CNT_THRESH = 30


def set_params(x,y,size):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size


def retrieve_params():

    return detected_x,detected_y,org_size

def reset():
    global detected_x
    global detected_y
    global is_flashing
    global no_flashing_cnt
    detected_x = 0
    detected_y = 0
    is_flashing = False
    no_flashing_cnt = 0


def run(last_valid_frame,frame):

    global no_flashing_cnt
    global is_flashing

    x,y,size,is_success = feature_detetor.detect_orange_btn(last_valid_frame,frame,detected_x,detected_y,org_size,2)

    is_detected = flash_detetor.flash_detection(last_valid_frame, frame, x, y,size)
    if is_flashing:
        # to detect when flash no longer flash in the recent 10 frames
        if is_detected:
            no_flashing_cnt = 0
        else:
            no_flashing_cnt += 1
    else:
        is_flashing = is_detected

    if no_flashing_cnt > NO_FLASHING_CNT_THRESH:
        reset()
        return True
    return False
