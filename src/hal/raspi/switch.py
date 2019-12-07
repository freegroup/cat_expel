import RPi.GPIO as GPIO
import time


class Switch:
    def __init__(self, name, pin):
        self.pin = pin
        self.name = name
        GPIO.setup(self.pin, GPIO.IN)

    def is_pressed(self):
        return GPIO.input(self.pin) == 1
