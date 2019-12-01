from hal.simulator.visual import put

class Motor:

    def __init__(self, name):
        self.wait_time = 0.001
        self.step_counter = 0
        self.name = name

    def off(self):
        pass

    def step(self, dir):
        self.step_counter += dir
        put({"value": 33})

