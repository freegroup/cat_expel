import RPi.GPIO as GPIO

from hal.raspi.motor import Motor
from hal.raspi.switch import Switch
import hal.raspi.camera as camera

class Hardware:
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    Camera = camera.Camera()

    Motor1 = Motor("motor1", 1, [17, 18, 27, 22])
    Motor2 = Motor("motor2", -1, [23, 24, 25, 4])
    Motor3 = Motor("motor3", 1, [13, 12, 6, 5])
    Motor4 = Motor("motor4", 1, [20, 26, 16, 19])

    Switch1 = Switch("switch1", 21)
    Switch2 = Switch("switch2", 7)
    Switch3 = Switch("switch3", 14)
    Switch4 = Switch("switch4", 15)


