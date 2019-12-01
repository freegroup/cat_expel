
from hal import Hardware, Mode
import time

hardware = Hardware()

class Switch:
    def __init__(self, pin, name="unknown"):
        self.pin = pin
        self.name = name
        hardware.setup(pin, Mode.IN)

    def pressed(self):
        return hardware.input(self.pin, self.name) == 1
   

if __name__ == "__main__":
    s = Switch(14)
    while True:
        print("pin pressed "+ str(s.pressed()))
        time.sleep(1)