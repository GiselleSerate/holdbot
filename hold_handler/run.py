#from proyximity import distance
from collections import deque
#from alert import blink, speak, wave
#import RPi.GPIO as GPIO
import time
from hold_handler import alert_action, reset_state, listen_action
import serial 

import offhold

CLASSIFY = False

if CLASSIFY: # tensorflow too long to load
    from .classifier import SmartClassifier, record
    classer = SmartClassifier()

#arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)

dist_q = deque(maxlen = 10)

def dance_forever():
    while True:
        try:
            alert_action()
            time.sleep(1)
            reset_state()
        except:
            pass

try:
   # reset_state()
    while True:
       print("HII")
       # print(distance())
       # dist_q.append(distance())
       while True:
       # while mean(dist_q) < 6.0:
       #     listen_action()
            if CLASSIFY:
                rec = record()
                is_hold = classer.classify(rec)
            else:
                is_hold = False
            if not is_hold:
               # print("alert")
                alert_action()
                time.sleep(0.1)
                listen_action()
                offhold.alert_offhold()
               # print("done alert")
                #speak()
            time.sleep(0.1)
except Exception as e:
    print(e)
    #reset_state()
    pass
