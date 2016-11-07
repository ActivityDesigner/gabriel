#
# Used for detecting stage two, namely to see if yellow plug has been plugged
# Created by haodong liu
#
import feature_detetor
import log

org_size = 0
detected_x = 0
detected_y = 0
frame_counter = 0

current_image = None
filter_image = None

def set_params(x,y,size_org):
    global detected_x
    global detected_y
    global org_size
    detected_x = x
    detected_y = y
    org_size = size_org


def reset():
    counter = 0


def get_two_image():
    return current_image,filter_image


def retrieve_params():

    return detected_x,detected_y,org_size


def run(last_valid_frame,frame):
    global detected_x
    global detected_y
    global org_size
    global frame_counter
    global current_image
    global filter_image

    print "stage-2"

    is_detected,x,y,size = feature_detetor.detect_yellow_plug(last_valid_frame, frame, detected_x, detected_y,org_size)
    detected_x = x
    detected_y = y
    org_size = size
    current_image, filter_image = feature_detetor.get_two_image()

    if is_detected == 1:
        reset()
        return True
    return False
