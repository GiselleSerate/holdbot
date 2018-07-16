#Libraries
import RPi.GPIO as GPIO
import time
import sounddevice as sd
import soundfile as sf


#GPIO.cleanup()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
#set GPIO Pins
GPIO_LEFT_EYE = 7
GPIO_RIGHT_EYE= 9

GPIO_LEFT_SPOON = 10
GPIO_RIGHT_SPOON = 11

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_LEFT_EYE, GPIO.OUT)
GPIO.setup(GPIO_RIGHT_EYE, GPIO.OUT)


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_LEFT_SPOON, GPIO.OUT)
GPIO.setup(GPIO_RIGHT_SPOON, GPIO.OUT)



def wave(times = 2):
    L = GPIO.PWM(GPIO_LEFT_SPOON, 50)
    R = GPIO.PWM(GPIO_RIGHT_SPOON, 50)
    L.start(7.5)
    R.start(7.5)
    for i in range(times):
        L.ChangeDutyCylce(7.5)
        R.ChangeDutyCylce(7.5)
        time.sleep(0.5)
        L.ChangeDutyCylce(12.5)
        R.ChangeDutyCylce(12.5)
        time.sleep(0.5)
        L.ChangeDutyCylce(2.5)
        R.ChangeDutyCylce(2.5)
        time.sleep(0.5)


def blink(times = 2):
    for i in range(times):
        GPIO.output(GPIO_RIGHT_EYE, 1)
        GPIO.output(GPIO_LEFT_EYE, 1)
        time.sleep(0.01)
        GPIO.output(GPIO_RIGHT_EYE, 0)
        GPIO.output(GPIO_LEFT_EYE, 0)

def speak():
    X, _ = sf.read('OFFHOLD.wav', dtype='float64')
    sd.play(X)
    sd.wait()

