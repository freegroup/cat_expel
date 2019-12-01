from hal.simulator.visual import put

steps = 64
ratio = 63.65 * (35/15)
steps_per_rotation = (360 / steps)*ratio

class Motor:

    def __init__(self, name):
        self.current_step = 0
        self.name = name

    def off(self):
        pass

    def step(self, dir):
        self.current_step += dir
        angle = (360/steps_per_rotation * self.current_step)%360
        put({"device": self.name, "angle": angle })


