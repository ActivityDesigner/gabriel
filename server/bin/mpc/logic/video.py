#
# The main logical loop for processing an video containing all needed AED operations.
#
import cv2
import util
import stage_pre_main
import stage_1_main
import stage_2_main
import stage_3_main


str1 = '../video/AED5.mp4'
cap = cv2.VideoCapture(str1)
while not cap.isOpened():
    cap = cv2.VideoCapture(str1)
    cv2.waitKey(1000)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
last_pos_frame = 1
frame_counter = 0
frame_sampling = 1

#
# Variables for each stage
#
CONST_STAGE_PREPARE = -1
CONST_STAGE_START = 0
CONST_STAGE_PLUG = 1
CONST_STAGE_FLASH_BTN = 2
CONST_STAGE_SHOCK_DELIVER = 3
current_stage = CONST_STAGE_PREPARE

detected_x = 0
detected_y = 0

while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        if pos_frame > last_pos_frame + frame_sampling:

            if frame_counter > 10:

                #last_valid_frame = util.getRotatedImage(last_valid_frame, [600, 300], [500, 500], [720, 380])
                #frame = util.getRotatedImage(frame, [600, 300], [500, 500], [720, 380])
                if current_stage == CONST_STAGE_PREPARE:
                    # do preposition
                    is_prepared = stage_pre_main.prepare(last_valid_frame,frame)
                    if is_prepared:
                        print "find the aed and well prepared, now turn to stage 1 detection"
                        current_stage = CONST_STAGE_START
                        detected_x,detected_y,size_org = stage_pre_main.retrieve_org_btn_params()
                        stage_1_main.set_org_params(detected_x,detected_y,size_org)

                elif current_stage == CONST_STAGE_START:
                    # do start stage detection
                    is_success = stage_1_main.run(last_valid_frame,frame)
                    if is_success:
                        print "detect the aed turn on, now turn to stage 2 detection"
                        current_stage = CONST_STAGE_PLUG
                        detected_x,detected_y,size_org = stage_1_main.retrieve_org_params()
                        stage_2_main.set_params(detected_x,detected_y,size_org)

                elif current_stage == CONST_STAGE_PLUG:
                    is_success = stage_2_main.run(last_valid_frame,frame)
                    if is_success:
                        print "detect the yellow plug, now turn to stage 3 detection"
                        current_stage = CONST_STAGE_FLASH_BTN
                        detected_x,detected_y,size_org = stage_2_main.retrieve_params()
                        stage_3_main.set_params(detected_x,detected_y,size_org)

                elif current_stage == CONST_STAGE_FLASH_BTN:
                    print "detect the flash button"
                    is_success = stage_3_main.run(last_valid_frame,frame)
                    if is_success:
                        print "detect the flash button, now turn to end"
                        current_stage = CONST_STAGE_SHOCK_DELIVER

                elif current_stage == CONST_STAGE_SHOCK_DELIVER:
                    print "CONST_STAGE_SHOCK_DELIVER"
                    break
            last_pos_frame = pos_frame
            last_valid_frame = frame
            frame_counter = frame_counter + 1
            print "#################### Frame counter" + str(frame_counter)
            if frame_counter == 100:
                util.show_two_image(last_valid_frame,frame)

    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
        print "frame is not ready"
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 32:
        break
    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break
