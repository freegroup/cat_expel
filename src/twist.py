import time

from hal import Hardware

while True:
    while not Hardware.Switch1.is_pressed():
        Hardware.Motor1.step(-1)
        time.sleep(0.001)

    while not Hardware.Switch2.is_pressed():
        Hardware.Motor1.step(1)
        time.sleep(0.001)
