

class Switch:

    def __init__(self, name, related_motor, end_angle):
        self.name = name
        self.related_motor = related_motor
        self.end_angle_low = end_angle-5
        self.end_angle_high = end_angle+5

    def is_pressed(self):
        angle = int(self.related_motor.get_angle())

        pressed = self.end_angle_low <= angle <= self.end_angle_high
        print(self.name, pressed, self.end_angle_low, angle)
        return pressed


