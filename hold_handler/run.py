from .proximity import distance
from .classifier import SmartClassifier, record
from .util import RingBuffer
from collections import deque 
from alert import blink, speak
import RPi.GPIO as GPIO
import time


dist_q = deque(maxlen = 10)
classer = SmartClassifier()

GPIO.cleanup()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_LEFT_EYE = 7
GPIO_RIGHT_EYE= 9
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_LEFT_EYE, GPIO.OUT)
GPIO.setup(GPIO_RIGHT_EYE, GPIO.OUT)

while True:
    dist_q.append(distance())
    while mean(dist_q) < 6.0:
        rec = record()
        is_hold = classer.classify(rec)
        if not is_hold:
            blink(GPIO_RIGHT_EYE, GPIO_LEFT_EYE)
            speak()
    time.sleep(0.1)