
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

class Switch:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin,GPIO.IN)

    def pressed(self):
        return GPIO.input(self.pin)==1
   

if __name__ == "__main__":
    s = Switch(14)
    while True:
        print("pin pressed "+ str(s.pressed()))
        time.sleep(1)