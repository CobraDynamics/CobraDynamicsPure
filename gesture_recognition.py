"""
    CobraDynamics / Oct 2024
    
    Jan Hildebrandt (https://github.com/abracodedabra)

    Kurzbeschreibung: Funktion zur Gestenerkennung, die einen int-Wert zurückgibt, um die Suche nach einem Ball auszulösen
"""

import cv2
import mediapipe as mp
from flask import Flask, Response
import numpy as np
from IPython.display import display, Image
import ipywidgets as widgets
from picamera2 import Picamera2

IMG_X_SIZE = 640
IMG_Y_SIZE = 480

from_all_out = None 
from_all_in = None 
from_thumb_up = None 
from_three_down = None 
from_thumb_down = None 
gesture = None

# Funktion zur Rückgabe der Geste, die durch Zahlenwerte die Suche in der Main triggert
def gesture_trigger(landmarks, mpHandss):
    
    direction = None
    thumb = None
    index = None
    middle = None
    ring = None
    pinky = None
    fld = 'folded'
    strd = 'streched'
    thup = None
    global gesture
    #gesture = gestureNone
    mpHands = mpHandss
    global from_all_out #
    global from_all_in #
    global from_thumb_up #
    global from_three_down #
    global from_thumb_down #


    # Setzt die Koordinaten der Landmarks in Pixel in den aktuellen Frame
    wrist = [landmarks[mpHands.HandLandmark.WRIST].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.WRIST].y * IMG_Y_SIZE]
    thumb_cmc = [landmarks[mpHands.HandLandmark.THUMB_CMC].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.THUMB_CMC].y * IMG_Y_SIZE]
    thumb_mcp = [landmarks[mpHands.HandLandmark.THUMB_MCP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.THUMB_MCP].y * IMG_Y_SIZE]
    thumb_ip = [landmarks[mpHands.HandLandmark.THUMB_IP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.THUMB_IP].y * IMG_Y_SIZE]
    thumb_tip = [landmarks[mpHands.HandLandmark.THUMB_TIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.THUMB_TIP].y * IMG_Y_SIZE]
    index_mcp = [landmarks[mpHands.HandLandmark.INDEX_FINGER_MCP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.INDEX_FINGER_MCP].y * IMG_Y_SIZE]
    index_pip = [landmarks[mpHands.HandLandmark.INDEX_FINGER_PIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.INDEX_FINGER_PIP].y * IMG_Y_SIZE]
    index_dip = [landmarks[mpHands.HandLandmark.INDEX_FINGER_DIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.INDEX_FINGER_DIP].y * IMG_Y_SIZE]
    index_tip = [landmarks[mpHands.HandLandmark.INDEX_FINGER_TIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.INDEX_FINGER_TIP].y * IMG_Y_SIZE]
    middle_mcp = [landmarks[mpHands.HandLandmark.MIDDLE_FINGER_MCP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.MIDDLE_FINGER_MCP].y * IMG_Y_SIZE]
    middle_pip = [landmarks[mpHands.HandLandmark.MIDDLE_FINGER_PIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.MIDDLE_FINGER_PIP].y * IMG_Y_SIZE]
    middle_dip = [landmarks[mpHands.HandLandmark.MIDDLE_FINGER_DIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.MIDDLE_FINGER_DIP].y * IMG_Y_SIZE]
    middle_tip = [landmarks[mpHands.HandLandmark.MIDDLE_FINGER_TIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y * IMG_Y_SIZE]
    ring_mcp = [landmarks[mpHands.HandLandmark.RING_FINGER_MCP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.RING_FINGER_MCP].y * IMG_Y_SIZE]
    ring_pip = [landmarks[mpHands.HandLandmark.RING_FINGER_PIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.RING_FINGER_PIP].y * IMG_Y_SIZE]
    ring_dip = [landmarks[mpHands.HandLandmark.RING_FINGER_DIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.RING_FINGER_DIP].y * IMG_Y_SIZE]
    ring_tip = [landmarks[mpHands.HandLandmark.RING_FINGER_TIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.RING_FINGER_TIP].y * IMG_Y_SIZE]
    pinky_mcp = [landmarks[mpHands.HandLandmark.PINKY_MCP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.PINKY_MCP].y * IMG_Y_SIZE]
    pinky_pip = [landmarks[mpHands.HandLandmark.PINKY_PIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.PINKY_PIP].y * IMG_Y_SIZE]
    pinky_dip = [landmarks[mpHands.HandLandmark.PINKY_DIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.PINKY_DIP].y * IMG_Y_SIZE]
    pinky_tip = [landmarks[mpHands.HandLandmark.PINKY_TIP].x * IMG_X_SIZE, landmarks[mpHands.HandLandmark.PINKY_TIP].y * IMG_Y_SIZE]

    # Erkennung der Handrichtung
    if wrist[0] > middle_mcp[0] and not wrist[1] > (middle_mcp[1] + 50) and wrist[0] > middle_mcp[0] and not wrist[1] < (middle_mcp[1] - 50):
        direction = 'left'
    elif wrist[0] < middle_mcp[0] and not wrist[1] > (middle_mcp[1] + 50) and wrist[0] < middle_mcp[0] and not wrist[1] < (middle_mcp[1] - 50):
        direction = 'right'
    elif wrist[1] < middle_mcp[1]:
        direction = 'down'
    elif wrist[1] > middle_mcp[1]:
        direction = 'up'

    # Entscheidung, ob ein Finger ausgestreckt oder herangezogen ist, basierend auf der Handrichtung
    if direction == 'left': 
        thumb = fld if thumb_mcp[1] < thumb_tip[1] else strd
        index = fld if index_pip[0] < index_tip[0] else strd
        middle = fld if middle_pip[0] < middle_tip[0] else strd
        ring = fld if ring_pip[0] < ring_tip[0] else strd
        pinky = fld if pinky_pip[0] < pinky_tip[0] else strd
    elif direction == 'right':
        thumb = fld if thumb_mcp[1] < thumb_tip[1] else strd
        index = fld if index_pip[0] > index_tip[0] else strd
        middle = fld if middle_pip[0] > middle_tip[0] else strd
        ring = fld if ring_pip[0] > ring_tip[0] else strd
        pinky = fld if pinky_pip[0] > pinky_tip[0] else strd
    elif direction == 'up':
        thumb = fld if thumb_mcp[0] < thumb_tip[0] else strd
        index = fld if index_pip[1] < index_tip[1] else strd
        middle = fld if middle_pip[1] < middle_tip[1] else strd
        ring = fld if ring_pip[1] < ring_tip[1] else strd
        pinky = fld if pinky_pip[1] < pinky_tip[1] else strd
    elif direction == 'down':
        thumb = fld if thumb_mcp[0] < thumb_tip[0] else strd
        index = fld if index_pip[1] > index_tip[1] else strd
        middle = fld if middle_pip[1] > middle_tip[1] else strd
        ring = fld if ring_pip[1] > ring_tip[1] else strd
        pinky = fld if pinky_pip[1] > pinky_tip[1] else strd

    # Definiert den Trigger für die Gestenerkennung
    allOut = 'all_out' if thumb == strd and index == strd and middle == strd and ring == strd and pinky == strd else None
    fourOut = 'four_out' if thumb == fld and index == strd and middle == strd and ring == strd and pinky == strd else None
    allIn = 'all_in' if thumb == fld and index == fld and middle == fld and ring == fld and pinky == fld else None
    thup = 'thumbs_up' if thumb == strd and index == fld and middle == fld and ring == fld and pinky == fld else None
    two = 'two' if thumb == strd and index == strd and middle == fld and ring == fld and pinky == fld else None
    three = 'three' if thumb == strd and index == strd and middle == strd and ring == fld and pinky == fld else None
    countUp = 'count_up' if thumb == fld and index == fld and middle == fld and ring == fld and pinky == fld else None
    #countDown = 'count_down' if thumb == strd and index == strd and middle == strd and ring == fld and pinky == fld else None

    # Entscheidung der Startgeste für die nachfolgende Erkennung der Endgeste
    if fourOut:
        from_all_out = True # Start für Thumbs up
    elif three and from_all_in == None: 
        from_three_down = True # Start für Count down
        from_all_in = False
    elif allIn:
        from_all_in = True # Start für Count up
        #from_all_out = False

    # Entscheidung, ob Geste Thumbs-up erkannt wird oder Thumbs up übergangen wird für Count-up oder Count-down
    if gesture == None and thup and from_all_out == True and not from_all_in:
        gesture = 1 # 1 = Thumbs up
        from_all_out = False
        from_all_in = False
    elif gesture == None and thup and from_all_out == None and from_three_down == True:
        from_thumb_down = True
        from_thumb_up = False
    elif gesture == None and thup and from_all_in == True:
        from_thumb_up = True
        from_thumb_down = False

    # Erkennung von Count-down 
    if gesture == None and allIn and from_thumb_down == True:
        gesture = 3 # 3 = Count down
        allIn = None
        from_all_in = False
    
    # Erkennung von Count-up
    if gesture == None and three and from_all_in == True and not from_all_out == True:
        gesture = 2 # 2 = Count up

    # Returnwert gibt eine Ganzzahl (int) zurück
    # 1 = Thumbs up
    # 2 = Count up
    # 3 = Count down
    return gesture