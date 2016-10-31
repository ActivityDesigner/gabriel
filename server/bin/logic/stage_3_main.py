#
# Used for detecting stage three, namely to see if orange button has been pressed
# Created by haodong liu
#
import flash_detetor

detected_x = 0
detected_y = 0
is_flashing = False
no_flashing_cnt = 0
NO_FLASHING_CNT_THRESH = 30


def set_params(x,y):
    global detected_x
    global detected_y
    detected_x = x
    detected_y = y


def retrieve_params():

    return detected_x,detected_y

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

    is_detected = flash_detetor.flash_detection(last_valid_frame, frame, detected_x, detected_y, 2)
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
