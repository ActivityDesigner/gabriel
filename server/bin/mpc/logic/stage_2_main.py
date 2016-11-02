#
# Used for detecting stage two, namely to see if yellow plug has been plugged
# Created by haodong liu
#
import feature_detetor


org_size = 0
detected_x = 0
detected_y = 0
frame_counter = 0


def set_params(x,y,size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org

def reset():
    counter = 0


def retrieve_params():

    return detected_x,detected_y,org_size


def run(last_valid_frame,frame):
    global detected_x
    global detected_y
    global org_size
    global frame_counter

    is_detected,x,y,size = feature_detetor.detect_yellow_plug(last_valid_frame, frame, detected_x, detected_y,org_size)
    detected_x = x
    detected_y = y
    org_size = size
    if is_detected == 1:
        reset()
        return True
    return False
