import threading
import random
import serial
import time
import math

#from .proximity import distance
#from .classifier import SmartClassifier, record
#from .util import RingBuffer

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

    hold_buffer_size = 10
    buff_bot_prop = 0.2
    buff_top_prop = 0.2
    hl_ringbuff = RingBuffer(hold_buffer_size)
    while True:
        if not hl_ringbuff.is_full:
            hl_ringbuff.add(distance())
            continue

        hl_ringbuff.pop()
        hl_ringbuff.add(distance())
        rb_vals = sorted(hl_ringbuff.buffer)
        bot_idx = math.floor(hold_buffer_size * buff_bot_prop)
        top_idx = hold_buffer_size - math.ceil(hold_buffer_size * buff_top_prop)
        sum_vals = 0
        for i in range(bot_idx, top_idx):
            sum_vals += hl_ringbuff.buffer[i]
        filtered_distance = sum_vals / hold_buffer_size
        cur_state = (filtered_distance <= 7.0)

        if _RUN_HOLD_HANDLER != cur_state:
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
        cur_recording = record()
        _CLF_CV.acquire()
        _CLF_QUEUE.append(cur_recording)
        _CLF_CV.release()

try:
    arduinoSerialData = serial.Serial('/dev/ttyACM1',9600)
except:
    arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)

def reset_state():
    global _RUN_HOLD_HANDLER
    global _CLF_QUEUE
    print("STATE BEING RESET")
    _RUN_HOLD_HANDLER = False
    _CLF_QUEUE = []
    arduinoSerialData.write(b'0')

def alert_action():
    arduinoSerialData.write(b'2')

def listen_action():
    arduinoSerialData.write(b'1')

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

        listen_action()

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
