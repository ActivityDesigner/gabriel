#
# Used for detecting stage one, namely to see if AED has been turned on
# Created by haodong liu
#
import flash_detetor
import feature_detetor

org_size = 0
detected_x = 0
detected_y = 0


def set_params(x, y,size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org



def retrieve_params():
    return detected_x, detected_y,org_size


# 1.detect the range of start btn
# 2.detect hand appearing in the range of start btn
# 3.detect flashing orange button in the next three frames, if happend, return true,
is_hand_appearing = False
hand_disappear_cnt = 0


def run(last_valid_frame,frame):

    start_btn_x,start_btn_y = feature_detetor.detect_start_btn(last_valid_frame,frame)

    hand_x,hand_y = feature_detetor.detect_hand(last_valid_frame,frame)

    print hand_x, hand_y

    global is_hand_appearing;
    global hand_disappear_cnt;
    global detected_x
    global detected_y
    global org_size
    is_hand_appearing = True

    # if abs(hand_x - start_btn_x) < 200 and abs(hand_y - start_btn_y) < 200:
    #     # the hand is right above the btn
    #     is_hand_appearing = True
    #     hand_disappear_cnt = 0
    # else:
    #     hand_disappear_cnt += 1
    #     if hand_disappear_cnt > 5:
    #         is_hand_appearing = False
    print "stage_1_start " + str(detected_x) +" "+ str(detected_y)+" "+str(org_size)
    is_flash_detected = False
    x,y,size = feature_detetor.detect_orange_btn(last_valid_frame,frame,detected_x,detected_y,org_size)
    detected_x = x
    detected_y = y
    org_size = size
    print "stage_1_end " + str(detected_x) +" "+ str(detected_y)+" "+str(org_size)
    if is_hand_appearing:
        return flash_detetor.flash_detection(last_valid_frame,frame,detected_x,detected_y,org_size)
    return False