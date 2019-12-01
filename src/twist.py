import time

from hal import Hardware

while True:
    for a in range(0,400):
        Hardware.Motor1.step(1)
        time.sleep(0.001)

    for a in range(0,400):
        Hardware.Motor1.step(-1)
        time.sleep(0.001)
