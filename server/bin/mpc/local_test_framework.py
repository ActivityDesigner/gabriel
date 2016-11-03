import cv2
import numpy as np
# import the necessary packages
import os
from os import listdir
from os.path import isfile, join
import imutils
from matplotlib import pyplot as plt
import threading
import csv
import aed_state_check
import tpod_state_check
import Queue
import collections
from optparse import OptionParser

# AED project
MAX_PIC_NUM = 100
PIC_QUEUE = collections.deque(maxlen=MAX_PIC_NUM)

# TPOD Parameters
TPOD_QUEUE = collections.deque(maxlen=2)

AEDStateCheck = aed_state_check.AEDState()
TPODStateCheck = tpod_state_check.TpodState()
is_running = True


class AEDThread(threading.Thread):
    def __init__(self):
        self.stop = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while (not self.stop.wait(0.01) and is_running):
            try:
                crt_pic = PIC_QUEUE.popleft()
                AEDStateCheck.logic(crt_pic)
            except IndexError as e:
                # stop for 10 ms if the queue is empty
                # print "[TPOD_CHECK_THREAD]: NO PICTURES in TPOD QUEUE " + str(len(PIC_QUEUE))
                self.stop.wait(0.1)
                continue


class TPODThread(threading.Thread):
    def __init__(self):
        self.stop = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while (not self.stop.wait(0.01) and is_running):
            try:
                crt_pic = TPOD_QUEUE.popleft()
                TPODStateCheck.logic(crt_pic)
            except IndexError as e:
                # stop for 10 ms if the queue is empty
                # print "[TPOD_CHECK_THREAD]: NO PICTURES in TPOD QUEUE " + str(len(PIC_QUEUE))
                self.stop.wait(0.1)
                continue


def main():
    # topdThread = TPODThread()
    aedThread = AEDThread()
    aedThread.start()
    # topdThread.start()
    is_running = True
    process_video()


def process_video():
    cap = cv2.VideoCapture("video/AED4.mp4")
    ret = True
    while ret:
        ret, frame = cap.read()
        if not frame:
            break
        target_width = 500.0
        fx = target_width / frame.shape[0]
        # resize image to 500 width
        frame = cv2.resize(frame, (0, 0), fx=fx, fy=fx)
        if AEDStateCheck.has_debug_image():
            cv2.imshow("Video", AEDStateCheck.get_debug_image())
        frame_process(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            ret = False
            break
    cap.release()
    cv2.destroyAllWindows()


def frame_process(frame):
    PIC_QUEUE.append(frame.copy())
    # TPOD_QUEUE.append(frame.copy())


# def process_image():
#     path = "button_train"
#     for r in listdir(path):
#         file_path = join(path, r)
#         if r.endswith("png") or r.endswith("jpg") or r.endswith("jpeg"):
#             # load the image and convert it to grayscale
#             image = cv2.imread(file_path)
#             frame_process(image)
#             cv2.waitKey(0)

main()
