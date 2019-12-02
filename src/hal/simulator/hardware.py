import multiprocessing

from hal.simulator.motor import Motor
from hal.simulator import visual
from hal.simulator.switch import Switch

# required
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

import random

class Hardware():

    # Open up our window
    queue = multiprocessing.Queue()
    visual.queue = queue

    p = multiprocessing.Process(target=visual.display, args=(queue,))
    p.start()

    Motor1 = Motor("motor1")
    Motor2 = Motor("motor2")
    Motor3 = Motor("motor3")
    Motor4 = Motor("motor4")

    Switch1 = Switch("switch1", Motor1, 40)
    Switch2 = Switch("switch2", Motor1, 210)
    Switch3 = Switch("switch3", Motor2, 10)
    Switch4 = Switch("switch4", Motor2, 210)

    # set some random angle for the different motors
    angle = random.randint(10, 200)
    Motor1.set_angle(angle)

