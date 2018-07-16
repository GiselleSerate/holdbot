#Libraries
import RPi.GPIO as GPIO
import time
import sounddevice as sd
import soundfile as sf


def blink(GPIO_RIGHT_EYE, GPIO_LEFT_EYE, times = 2):
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

