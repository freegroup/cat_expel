from hal.simulator.visual import execute

steps = 64
ratio = 63.65 * (35 / 15)
steps_per_rotation = (steps * ratio)

class Motor:

    def __init__(self, name):
        self.current_step = 0
        self.angle = 0
        self.name = name

    def off(self):
        pass

    def set_null(self):
        self.angle = 0
        self.current_step = 0

    def set_angle(self, angle):
        self.angle = angle
        self.current_step = int(steps_per_rotation * angle) / 360
        execute({"command": self.name + "_set_angle", "value": self.angle})

    def get_angle(self):
        return self.angle

    def step(self, dir):
        self.current_step += dir
        self.angle = ((360 / steps_per_rotation) * self.current_step) % 360
        execute({"command": self.name + "_set_angle", "value": self.angle})
