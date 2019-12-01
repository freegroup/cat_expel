import time

from hal import Hardware

while True:
    Hardware.Motor1.step(1)
    time.sleep(0.004)
