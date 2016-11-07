import multiprocessing
import Queue
import collections
from optparse import OptionParser
import os
import pprint
import struct
import time
import threading
import pdb
import sys
import json
import cv2
import numpy as np
import base64
import requests
import logic.util as util
import logic.stage_pre_main as stage_pre_main
import logic.stage_1_main as stage_1_main
import logic.stage_2_main as stage_2_main
import logic.stage_3_main as stage_3_main
import logic.log as log

AED_PREPARE = -1
AED_START = 0
AED_ON = 1
AED_PULGIN = 2
AED_SHOCK = 3


TAG = "MAIN"

class AEDState:
    speech_message = {
        AED_PREPARE: "Please look at AED, begin cognitive assistant soon",
        AED_START: "Please turn on AED.",
        AED_ON: "Nice! Now apply pad and plug in",
        AED_PULGIN: "Congratulations, now wait for further instructions",
        AED_SHOCK: "Press orange button to deliver shock"
    }

    def __del__(self):
        log.close_all()

    def __init__(self):
        # AED STATE
        self.CURRENT_AED_STATE = AED_PREPARE
        self.last_pic = None
        self.frame_counter = 0
        self.debug_image = None
        self.debug_image2 = None
        self.image_prepare_1 = None
        self.image_prepare_2 = None
        self.image_turn_on_1 = None
        self.image_turn_on_2 = None
        self.image_plug_in_1 = None
        self.image_plug_in_2 = None
        self.image_shock_1 = None
        self.image_shock_2 = None

    def has_debug_image(self):
        return self.debug_image != None

    def has_debug_image2(self):
        return self.debug_image2 != None

    def get_debug_image(self):
        return self.debug_image

    def get_debug_image2(self):
        return self.debug_image2

    def get_speech_message(self):
        return self.speech_message[self.CURRENT_AED_STATE]

    def logic(self, image):
        # define your global vars here..
        try:
            crt_pic = image
            if self.frame_counter > 10:
                #self.debug_image = crt_pic
                if self.CURRENT_AED_STATE == AED_PREPARE:
                    # do preposition
                    is_prepared = stage_pre_main.prepare(self.last_pic, crt_pic)
                    self.debug_image,self.debug_image2 = stage_pre_main.get_two_image()
                    if is_prepared:
                        image_prepare = stage_pre_main.get_contour_image()
                        log.print_info(TAG,"at frame "+str(self.frame_counter)+" find the aed and well prepared, now turn to stage 1 detection")
                        self.CURRENT_AED_STATE = AED_START
                        detected_x, detected_y, size_org = stage_pre_main.retrieve_org_btn_params()
                        stage_1_main.set_org_params(detected_x, detected_y, size_org)

                elif self.CURRENT_AED_STATE == AED_START:
                    # do start stage detection
                    is_success = stage_1_main.run(self.last_pic, crt_pic)
                    self.debug_image,self.debug_image2 = stage_1_main.get_two_image()
                    if is_success:
                        log.print_info(TAG,"at frame "+str(self.frame_counter)+" detect the aed turn on, now turn to stage 2 detection")
                        self.CURRENT_AED_STATE = AED_ON
                        detected_x, detected_y, size_org = stage_1_main.retrieve_org_params()
                        stage_2_main.set_params(detected_x, detected_y, size_org)
                        self.image_turn_on_1, self.image_turn_on_2 = stage_1_main.get_two_image()

                elif self.CURRENT_AED_STATE == AED_ON:
                    is_success = stage_2_main.run(self.last_pic, crt_pic)
                    self.debug_image,self.debug_image2 = stage_2_main.get_two_image()
                    if is_success:
                        log.print_info(TAG,"at frame "+str(self.frame_counter)+" detect the yellow plug, now turn to stage 3 detection")
                        self.CURRENT_AED_STATE = AED_PULGIN
                        detected_x, detected_y, size_org = stage_2_main.retrieve_params()
                        stage_3_main.set_params(detected_x, detected_y, size_org)
                        self.image_plug_in_1, self.image_plug_in_2 = stage_2_main.get_two_image()

                elif self.CURRENT_AED_STATE == AED_PULGIN:
                    is_success = stage_3_main.run(self.last_pic, crt_pic)
                    self.debug_image,self.debug_image2 = stage_3_main.get_two_image()

                    if is_success:
                        log.print_info(TAG,"detect the flash button, now turn to end")
                        self.CURRENT_AED_STATE = AED_SHOCK
                        self.image_shock_1, self.image_shock_2 = stage_3_main.get_two_image()

                elif self.CURRENT_AED_STATE == AED_SHOCK:
                    log.print_info(TAG, "shock delivered")

            self.frame_counter += 1
            log.print_debug(TAG,"frame counter " + str(self.frame_counter))
            self.last_pic = crt_pic

        except IndexError as e:
            print e
