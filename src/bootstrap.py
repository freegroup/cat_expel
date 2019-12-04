import time

from hal import Hardware

def bootstrap():
    init_gimbal()


def init_gimbal():
    sweep_steps = 0

    print("sweep gimbal to the left")
    while not Hardware.Switch1.is_pressed():
        Hardware.Motor1.step(-1)
        time.sleep(0.001)

    print("sweep gimbal to the right")
    while not Hardware.Switch2.is_pressed():
        sweep_steps=sweep_steps+1
        Hardware.Motor1.step(1)
        time.sleep(0.001)

    print("center gimbal")
    center_sweep = int(sweep_steps/2)
    while center_sweep > 0:
        Hardware.Motor1.step(-1)
        time.sleep(0.001)
        center_sweep = center_sweep-1


if __name__ == "__main__":
    bootstrap()