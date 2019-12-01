import multiprocessing
import time
from hal.simulator.motor import Motor
from  hal.simulator import visual

# required
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES



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

