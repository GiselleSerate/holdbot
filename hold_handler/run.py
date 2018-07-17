from proximity import distance
from collections import deque
from alert import blink, speak, wave
from numpy import mean

import RPi.GPIO as GPIO
import time
#from hold_handler import alert_action, reset_state, listen_action
import serial 

#import offhold

CLASSIFY = True

if CLASSIFY: # tensorflow too long to load
    from classifier import SmartClassifier, record
    classer = SmartClassifier()

#arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)

dist_q = deque(maxlen = 10)

try:
    while True:
       dist = int(distance())
#       print(dist)
       dist_q.append(dist)
       while mean(dist_q) < 8.0:
            if CLASSIFY:
                rec = record()
                is_hold = classer.classify(rec)
            else:
                is_hold = False
            if not is_hold:
                print("alert")
                wave(1)
                blink()
            time.sleep(0.1)
            break
except Exception as e:
    GPIO.cleanup()
    print(e)
    pass
