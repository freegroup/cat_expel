import multiprocessing
import time
import os

from hal.simulator.motor import Motor
from hal.simulator import visual
from hal.simulator.switch import Switch
import hal.simulator.camera as camera
from file.configuration import Configuration

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(CWD_PATH, "hardware.ini"))

# required
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

import random

class Hardware():

    switch1_angle = conf.get_int(section="axis_x", key="start_angle")
    switch2_angle = conf.get_int(section="axis_x", key="end_angle")
    switch3_angle = conf.get_int(section="axis_y", key="start_angle")
    switch4_angle = conf.get_int(section="axis_y", key="end_angle")

    # Open up our window
    queue = multiprocessing.Queue(100)
    visual.queue = queue

    p = multiprocessing.Process(target=visual.display, args=(queue,))
    p.start()

    Camera = camera.Camera()

    Motor1 = Motor("motor1")
    Motor2 = Motor("motor2")
    Motor3 = Motor("motor3")
    Motor4 = Motor("motor4")

    Switch1 = Switch("switch1", Motor1, switch1_angle)
    Switch2 = Switch("switch2", Motor1, switch2_angle)
    Switch3 = Switch("switch3", Motor2, switch3_angle)
    Switch4 = Switch("switch4", Motor2, switch4_angle)

    # set some random angle for the different motors
    angle = random.randint(switch1_angle, switch2_angle)
    Motor1.set_angle(angle)

    # wait until the UI is up and running
    time.sleep(1)

