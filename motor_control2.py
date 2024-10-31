#!/usr/bin/env python

"""
CobraDynamics
Martin Schottler
Oct 2024
"""

import time
import clr_recog as cr #detect_object
from base_ctrl import BaseController

MIN_DISTANCE = 340 # 20 cm distance
MIN_SPEED_METERS_PER_SECOND = 0.1
MAX_SPEED__METERS_PER_SECOND = 0.2
LIMT_RIGHT = 360
LIMT_LEFT = 280
IMG_X_SIZE = 640
IMG_Y_SIZE = 480
NONE_COORDINATE = -1

# Raspberry Pi 5 not supported
base = BaseController('/dev/serial0', 115200)


"""
Standard commands for controlling the rover
"""

def rotate_right():
    #print("rotate right")
    base.send_command({"T":1,"L":0.1,"R":-0.1})


def rotate_left():
    #print("rotate left")
    base.send_command({"T":1,"L":-0.1,"R":0.1})


def forwards():
    #print("forwards")
    base.send_command({"T":1,"L":0.1,"R":0.1})


def stop():
    #print("stop")
    base.send_command({"T":1,"L":0.0,"R":0.0})


def backwards():
    #print("backwards")
    base.send_command({"T":1,"L":-0.1,"R":-0.1})


def motor_test():
    """
    The wheel rotates at a speed of 0.2 meters per second and stops after 2 seconds.
    """
    base.send_command({"T":1,"L":0.2,"R":0.2})
    time.sleep(2)
    base.send_command({"T":1,"L":0,"R":0})
    #print("motor ctrl test")


def motor_control(cx, cy):
    """
    Drive in the direction of the object and stop 0.2m before it.

    Parameters
    ----------
        cx, cy Coordinates of the object
    """
    if cy > MIN_DISTANCE:
        """
        Distance to target reached
        """
        stop()
        time.sleep(2)
        #print("success")
        return True
    elif cx == NONE_COORDINATE and cy == NONE_COORDINATE:
        """
        No object detected, start searching
        """
        #print("searching for object...")
        rotate_left()
        time.sleep(0.5)
        stop()
        time.sleep(2)
    else:
        """
        Alignment to the object takes place here
        """
        if cx < LIMT_LEFT:
            rotate_left()
        elif cx > LIMT_RIGHT:
            rotate_right()
        else:
            forwards()