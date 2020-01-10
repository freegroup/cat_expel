import time


class Axis():

    def __init__(self, motor1, motor2=None):
        self.motor1 = motor1
        self.motor2 = motor2

    def center(self):
        print("center...")
        self.set_angle(0)

    def set_angle(self, angle):
        angle = angle+150
        print(angle)
        self.motor1.set_angle(angle)
        if self.motor2 is not None:
            self.motor2.set_angle(angle)
 
    def off(self):
        self.set_angle(0)
