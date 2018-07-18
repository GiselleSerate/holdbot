#!/usr/bin/env python3
from proximity import distance
from collections import deque
from alert import blink, speak, wave, freakout
from numpy import mean

import RPi.GPIO as GPIO
import time
import serial 

CLASSIFY = True

if CLASSIFY: # tensorflow too long to load
    from classifier import SmartClassifier, record
    classer = SmartClassifier()


dist_q = deque(maxlen = 10)

try:
    while True:
       dist = int(distance())
#       print(dist)
       dist_q.append(dist)
       if mean(dist_q) < 8.0:
            if CLASSIFY:
                rec = record()
                is_hold = classer.classify(rec)
            else:
                is_hold = False
            if not is_hold:
                print("alert")
                freakout(1)
            time.sleep(0.01)
except Exception as e:
    GPIO.cleanup()
    print(e)
    pass