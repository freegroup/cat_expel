from hal.simulator.visual import execute
import threading
import time


class Switch(threading.Thread):

    def __init__(self, name, related_motor, pos_angle):
        threading.Thread.__init__(self)
        self.name = name
        self.related_motor = related_motor
        self.end_angle_low = pos_angle - 5
        self.end_angle_high = pos_angle + 5
        execute({"command": self.name + "_set_pos_angle", "value": pos_angle})
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            self.is_pressed()
            time.sleep(0.001)

    def is_pressed(self):
        angle = int(self.related_motor.get_angle())
        pressed = self.end_angle_low <= angle <= self.end_angle_high
        execute({"command": self.name + "_set_pressed", "value": pressed})

        return pressed
