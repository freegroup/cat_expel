
from hal import Hardware, Mode
import time

hardware = Hardware()

class Switch:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        hardware.setup(pin, Mode.IN)

    def is_pressed(self):
        return hardware.input(self.pin, self.name) == 1
   
