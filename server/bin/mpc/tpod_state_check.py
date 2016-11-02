import multiprocessing
import Queue
import collections
from optparse import OptionParser
import os
import pprint
import struct
import sys
import time
import threading
import pdb

import json
import cv2
import numpy as np
import base64
import requests

TPOD_SCORE_THRESHOLD = 0.98
TPOD_PORT = 48486

class TpodState():
    def __init__(self):
        self.objects = {'aed': TPOD_PORT}
        self.TPOD_RESULT = False
        self.TPOD_AREA = None

    def logic(self, image):
        # define your global vars here..
        crt_pic = image
        results = self.object_detection_topd(crt_pic)
        if results is not None and results['confidence'] >= TPOD_SCORE_THRESHOLD:
            self.TPOD_RESULT = True
            self.TPOD_AREA = results['area']
        else:
            self.TPOD_RESULT = False
        print "[TPOD_CHECK_THREAD]: send request to TPOD, current state: " + str(self.TPOD_RESULT)

    def get_area(self):
        return self.TPOD_AREA

    def get_result(self):
        return self.TPOD_RESULT

    def object_detection_topd(self, pic):
        cv2.imwrite("temp.jpg", pic)
        for object, port in self.objects.iteritems():
            files = {'picture': open('temp.jpg', 'rb')}
            r = requests.post("http://cloudlet001.elijah.cs.cmu.edu:" + str(port) + "/0", files=files)
            response = eval(r.content)
            if r.status_code != 500 and len(response) > 0:
                os.remove("temp.jpg")
                area = response[0][1]
                confidence = float(response[0][2])
                return {'feature': object, 'confidence': confidence, 'area': area}
        return None

