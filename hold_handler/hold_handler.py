import threading
import random

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

    while True:
        rand = random.random()
        if rand > 0.2:

            #Inform main handler
            _HOLD_LISTENER_CV.acquire()
            _RUN_HOLD_HANDLER = True
            _HOLD_LISTENER_CV.notifyAll()
            _HOLD_LISTENER_CV.release()
            return

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

def send_alert():
    print("ALERT!")

def run_handler():
    global _RUN_HOLD_HANDLER
    global _HOLD_LISTENER_CV
    global _CLF_QUEUE
    global _CLF_CV

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
        cur_input = _CLF_QUEUE.pop()
        _RUN_HOLD_HANDLER = classify_input(classifier, cur_input)
        _CLF_CV.release()

    #Assume that now off hold and should alert
    send_alert()

run_handler()
