import RPi.GPIO as GPIO

from hal.raspi.motor import Motor
from hal.raspi.switch import Switch

class Hardware:
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    Motor1 = Motor("motor1", [17, 18, 27, 22])
    Motor2 = Motor("motor2", [23, 24, 25, 4])
    Motor3 = Motor("motor3", [13, 12, 6, 5])
    Motor4 = Motor("motor4", [20, 26, 16, 19])

    Switch1 = Switch(14, "switch1")
    Switch2 = Switch(15, "switch2")
    Switch3 = Switch(21, "switch2")
    Switch4 = Switch(7, "switch2")

