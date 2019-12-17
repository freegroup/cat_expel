import time
import threading


class Axis(threading.Thread):

    def __init__(self, motor1, motor2, endswitch_left, endswitch_right):
        threading.Thread.__init__(self)
        self.motor1 = motor1
        self.motor2 = motor2
        self.endswitch_left = endswitch_left
        self.endswitch_right = endswitch_right

        self.calibrated_0_angle = 0
        self.target_angle = 0

    def calibrate(self):
        print("calibrate...")
        sweep_steps = 0

        while not self.endswitch_left.is_pressed():
            self.motor1.step(-1)
            self.motor2.step(-1)
            time.sleep(0.001)

        while not self.endswitch_right.is_pressed():
            sweep_steps = sweep_steps + 1
            self.motor1.step(1)
            self.motor2.step(1)
            time.sleep(0.001)

        center_sweep = int(sweep_steps / 2)
        while center_sweep > 0:
            self.motor1.step(-1)
            self.motor2.step(-1)
            time.sleep(0.001)
            center_sweep = center_sweep - 1

        self.calibrated_0_angle = self.motor1.get_angle()
        self.target_angle = self.calibrated_0_angle
        self.setDaemon(True)
        self.start()

    def set_target_angle(self, angle):
        self.target_angle = angle

    def get_target_angle(self):
        return self.target_angle

    def get_current_angle(self):
        return self.motor1.get_angle() - self.calibrated_0_angle

    def off(self):
        self.motor1.off()
        self.motor2.off()

    def run(self):
        while True:
            current_angle = self.get_current_angle()
            if not ((self.target_angle - 1) <= current_angle <= (self.target_angle + 1)):
                if self.target_angle > current_angle and not self.endswitch_right.is_pressed():
                    self.motor1.step(1)
                    self.motor2.step(1)
                elif self.target_angle < current_angle and not self.endswitch_left.is_pressed():
                    self.motor1.step(-1)
                    self.motor2.step(-1)
            time.sleep(0.001)
