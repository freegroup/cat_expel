import RPi.GPIO as GPIO

# Define simple sequence
Seq1 = [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]

# Define advanced sequence
# as shown in manufacturers datasheet
Seq2 = [[1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]]

# Full torque
Seq3 = [[0, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 0]]

Seq = Seq2

steps = 64
ratio = 63.65 * (35 / 15)
steps_per_rotation = (steps * ratio)

class Motor:

    def __init__(self, name, dir, pins):
        self.step_pins = pins
        self.name = name
        self.dir = dir
        self.current_step = 0
        self.angle = 0

        # Set all pins as output
        for pin in self.step_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        self.step_count = len(Seq)
        self.wait_time = 0.001

        # Initialise variables
        self.step_counter = 0

    def off(self):
        # Set all pins as output
        for pin in self.step_pins:
            GPIO.output(pin, False)

    def set_angle(self, angle):
        self.angle = angle
        self.current_step = int(steps_per_rotation * angle) / 360

    def get_angle(self):
        return self.angle

    def step(self, dir):
        for index in range(0, 4):
            xpin = self.step_pins[index]  #
            xvalue = Seq[self.step_counter][index]
            GPIO.output(xpin, xvalue)
        dir = dir * self.dir
        self.step_counter += dir

        # If we reach the end of the sequence
        # start again
        if self.step_counter >= self.step_count:
            self.step_counter = 0

        if self.step_counter < 0:
            self.step_counter = self.step_count + dir

        self.current_step += dir
        self.angle = ((360 / steps_per_rotation) * self.current_step) % 360
