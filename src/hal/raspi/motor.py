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


class Motor:

    def __init__(self, name, pins):
        self.step_pins = pins
        self.name = name

        # Set all pins as output
        for pin in self.step_pins:
            GPIO.setup(pin, GPIO.OUT, self.name)
            GPIO.output(pin, False, self.name)

        self.step_count = len(Seq)
        self.wait_time = 0.001

        # Initialise variables
        self.step_counter = 0

    def off(self):
        # Set all pins as output
        for pin in self.step_pins:
            GPIO.output(pin, False)

    def step(self, dir):
        for index in range(0, 4):
            xpin = pin[index]  #
            xvalue = Seq[self.step_counter][index]
            GPIO.output(xpin, xvalue)
        self.step_counter += dir

        # If we reach the end of the sequence
        # start again
        if self.step_counter >= self.step_count:
            self.step_counter = 0

        if self.step_counter < 0:
            self.step_counter = self.step_count + dir
