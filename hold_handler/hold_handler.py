import threading
import random
import serial

from .proximity import distance

#TODO: Add GPIO i/o
#TODO: Add classifier

_RUN_HOLD_HANDLER = False
_HOLD_LISTENER_CV = threading.Condition()
_CLF_QUEUE = []
_CLF_CV = threading.Condition()

class DummyClassifier:
    def classify(self, data):
        rand = random.random()
        if rand > 0.6:
            return True
        else:
            return False

def hold_listener():
    global _RUN_HOLD_HANDLER
    global _HOLD_LISTENER_CV
    global _CLF_CV

    while True:
        cur_state = (distance() < 7.0)
        if _RUN_HOLD_HANDLER != cur_state:
            _HOLD_LISTENER_CV.acquire()
            _RUN_HOLD_HANDLER = cur_state
            if not cur_state:
                _CLF_CV.acquire()
                _CLF_CV.notifyAll()
                _CLF_CV.release()
            _HOLD_LISTENER_CV.notifyAll()
            _HOLD_LISTENER_CV.release()

def classify_input(classifier, data):
    return classifier.classify(data)

def get_input():
    global _RUN_HOLD_HANDLER
    global _CLF_CV
    global _CLF_QUEUE

    while (_RUN_HOLD_HANDLER):
        rand = random.random()
        if rand > 0.6:
            _CLF_CV.acquire()
            _CLF_QUEUE.append("dummy")
            _CLF_CV.release()

def reset_state():
    global _RUN_HOLD_HANDLER
    global _CLF_QUEUE

    _RUN_HOLD_HANDLER = False
    _CLF_QUEUE = []

arduinoSerialData = serial.Serial('/dev/ttyS3',9600)

def alert_action():
    global _RUN_HOLD_HANDLER

    currTime = int(round(time.time()))

    while _RUN_HOLD_HANDLER:
        oldTime = currTime
        currTime = int(round(time.time()))
        if(oldTime == currTime):
            continue
        if currTime % 10 == 5:
            arduinoSerialData.write('1')
        elif currTime % 10 == 0:
            arduinoSerialData.write('0')

def send_alert():
    print("ALERT!")
    alert_action()

def run_handler():
    global _RUN_HOLD_HANDLER
    global _HOLD_LISTENER_CV
    global _CLF_QUEUE
    global _CLF_CV

    while True:
        #Run hold activate listener
        hl_thread = threading.Thread(target=hold_listener)
        hl_thread.start()

        _HOLD_LISTENER_CV.acquire()
        while (not _RUN_HOLD_HANDLER):
            _HOLD_LISTENER_CV.wait()
        _HOLD_LISTENER_CV.release()

        #Start listening for new data
        gi_thread = threading.Thread(target=get_input)
        gi_thread.start()

        #Begin classifying incoming data
        classifier = DummyClassifier()
        while (_RUN_HOLD_HANDLER):
            _CLF_CV.acquire()
            while (not _CLF_QUEUE):
                _CLF_CV.wait()
            if not _RUN_HOLD_HANDLER:
                break
            cur_input = _CLF_QUEUE.pop()
            _RUN_HOLD_HANDLER = classify_input(classifier, cur_input)
            _CLF_CV.release()

        #Assume that now off hold and should alert
        if _RUN_HOLD_HANDLER:
            send_alert()

        reset_state()
