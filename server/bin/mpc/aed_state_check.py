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

AED_PREPARE = -1
AED_START = 0
AED_ON = 1
AED_PULGIN = 2
AED_SHOCK = 3


class AEDState:
    def __init__(self):
        # AED STATE
        self.CURRENT_AED_STATE = AED_PREPARE
        self.last_pic = None
        self.frame_counter = 0

    def logic(self, image):
        # define your global vars here..
        try:
            crt_pic = image
            # print "[AED THREAD] current frame:" + str(frame_counter)
            if self.frame_counter > 10:
                print "state" + str(self.CURRENT_AED_STATE)
                if self.CURRENT_AED_STATE == AED_PREPARE:
                    # do preposition
                    is_prepared = stage_pre_main.prepare(self.last_pic, crt_pic)
                    if is_prepared:
                        print "find the aed and well prepared, now turn to stage 1 detection"
                        self.CURRENT_AED_STATE = AED_START
                        detected_x, detected_y = stage_pre_main.retrieve_pos()
                        size_org = stage_pre_main.retrieve_size()
                        stage_1_main.set_params(detected_x, detected_y, size_org)

                elif self.CURRENT_AED_STATE == AED_START:
                    # do start stage detection
                    is_success = stage_1_main.run(self.last_pic, crt_pic)
                    if is_success:
                        print "detect the aed turn on, now turn to stage 2 detection"
                        self.CURRENT_AED_STATE = AED_ON
                        detected_x, detected_y, size_org = stage_1_main.retrieve_params()
                        stage_2_main.set_params(detected_x, detected_y, size_org)

                elif self.CURRENT_AED_STATE == AED_ON:
                    is_success = stage_2_main.run(self.last_pic, crt_pic)
                    if is_success:
                        print "detect the yellow plug, now turn to stage 3 detection"
                        self.CURRENT_AED_STATE = AED_PULGIN
                        detected_x, detected_y, size_org = stage_2_main.retrieve_params()
                        stage_3_main.set_params(detected_x, detected_y)

                elif self.CURRENT_AED_STATE == AED_PULGIN:
                    print "detect the flash button"
                    is_success = stage_3_main.run(self.last_pic, crt_pic)
                    if is_success:
                        print "detect the flash button, now turn to end"
                        self.CURRENT_AED_STATE = AED_SHOCK

                elif self.CURRENT_AED_STATE == AED_SHOCK:
                    print "CONST_STAGE_SHOCK_DELIVER"

            self.frame_counter += 1
            self.last_pic = crt_pic

        except IndexError as e:
            print e
