import threading
import random
import serial
import time

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
        if rand > 0.9:
            return True
        else:
            return False

def hold_listener():
    global _RUN_HOLD_HANDLER
    global _HOLD_LISTENER_CV
    global _CLF_CV

    #Just for preventing spurious changes
    change_threshold = 3
    num_con_changes = 0
    while True:
        cur_state = (distance() < 7.0)
        time.sleep(0.5)
        if _RUN_HOLD_HANDLER != cur_state:
            num_con_changes += 1
            if num_con_changes < change_threshold:
                continue
            num_con_changes = 0
            _HOLD_LISTENER_CV.acquire()
            _RUN_HOLD_HANDLER = cur_state
            if not cur_state:
                _CLF_CV.acquire()
                _CLF_CV.notifyAll()
                _CLF_CV.release()
            print("LISTENER NOTIFIED, RHH IS", _RUN_HOLD_HANDLER)
            _HOLD_LISTENER_CV.notifyAll()
            _HOLD_LISTENER_CV.release()

def classify_input(classifier, data):
    return classifier.classify(data)

def get_mic_input():
    global _RUN_HOLD_HANDLER
    global _CLF_CV
    global _CLF_QUEUE
    global _HOLD_LISTENER_CV

    while (True):
        _HOLD_LISTENER_CV.acquire()
        while (not _RUN_HOLD_HANDLER):
            _HOLD_LISTENER_CV.wait()
        _HOLD_LISTENER_CV.release()
        rand = random.random()
        if rand > 0.6:
            _CLF_CV.acquire()
            _CLF_QUEUE.append("dummy")
            _CLF_CV.release()

def reset_state():
    global _RUN_HOLD_HANDLER
    global _CLF_QUEUE

    print("STATE BEING RESET")
    _RUN_HOLD_HANDLER = False
    _CLF_QUEUE = []

arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)

def alert_action():
    global _RUN_HOLD_HANDLER

    currTime = int(round(time.time()))

    while _RUN_HOLD_HANDLER:
        oldTime = currTime
        currTime = int(round(time.time()))
        if(oldTime == currTime):
            continue
        if currTime % 10 == 5:
            arduinoSerialData.write(b'1')
        elif currTime % 10 == 0:
            arduinoSerialData.write(b'0')

def send_alert():
    print("ALERT!")
    alert_action()

def run_handler():
    global _RUN_HOLD_HANDLER
    global _HOLD_LISTENER_CV
    global _CLF_QUEUE
    global _CLF_CV

    classifier = DummyClassifier()

    #Run hold activate listener
    hl_thread = threading.Thread(target=hold_listener)
    hl_thread.start()
    gmi_thread = threading.Thread(target=get_mic_input)
    gmi_thread.start()

    while True:
        _HOLD_LISTENER_CV.acquire()
        while (not _RUN_HOLD_HANDLER):
            print("IN MAIN LOOP, HOLD CV")
            _HOLD_LISTENER_CV.wait()
        _HOLD_LISTENER_CV.release()

        print("PRE PROCESS")

        #Begin classifying incoming data
        while (_RUN_HOLD_HANDLER):
            _CLF_CV.acquire()
            while (not _CLF_QUEUE):
                print("WAITING TO PROCESS CLF DATA")
                _CLF_CV.wait()
            if not _RUN_HOLD_HANDLER:
                print("EXITING CLF PROCESSING")
                break
            print("IN INPUT PROCESSING")
            cur_input = _CLF_QUEUE.pop()
            is_hold = classify_input(classifier, cur_input)
            _CLF_CV.release()
            if not is_hold:
                break

        print("EXITING PROCESSING")
        #Assume that now off hold and should alert
        if _RUN_HOLD_HANDLER:
            print("SENDING ALERT")
            send_alert()
        else:
            print("EARLY TERMINATION")

        reset_state()
