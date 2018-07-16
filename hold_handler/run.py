from .proximity import distance
from .classifier import SmartClassifier, record
from .util import RingBuffer
from collections import deque 
from .alert import blink, speak
import RPi.GPIO as GPIO
import time


dist_q = deque(maxlen = 10)
classer = SmartClassifier()

while True:
    dist_q.append(distance())
    while mean(dist_q) < 6.0:
        rec = record()
        is_hold = classer.classify(rec)
        if not is_hold:
            wave()
            blink()
            speak()
    time.sleep(0.1)