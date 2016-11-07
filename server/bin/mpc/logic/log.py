
INFO_FILE_NAME = "info.txt"
DEBUG_FILE_NAME = "debug.txt"
ERROR_FILE_NAME = "error.txt"

f_info = None
f_error = None
f_debug = None

def print_info(TAG, msg):
    global f_info
    if f_info == None:
        f_info = open(INFO_FILE_NAME, 'w+')
    f_info.write(TAG+" "+msg+"\n")


def print_debug(TAG, msg):
    global f_debug
    if f_debug == None:
        f_debug = open(DEBUG_FILE_NAME, 'w+')
    f_debug.write(TAG+" "+msg+"\n")


def print_error(TAG, msg):
    global f_error
    if f_error == None:
        f_error = open(ERROR_FILE_NAME, 'w+')
    f_error.write(TAG+" "+msg+"\n")


def close_all():
    global f_info
    global f_error
    global f_debug
    if f_info != None:
        f_info.close()
        f_info = None
    if f_error != None:
        f_error.close()
        f_error = None
    if f_debug != None:
        f_debug.close()
        f_debug = None