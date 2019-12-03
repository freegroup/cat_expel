import math
import os
import threading
import time

from file.configuration import Configuration

SWEEP_LENGTH = 80

queue = None

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(CWD_PATH, "simulator.ini"))


class Commander(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.motor1_angle = 0
        self.motor2_angle = 0
        self.motor3_angle = 0
        self.motor4_angle = 0
        self.switch1_pressed = 0
        self.switch2_pressed = 0
        self.switch3_pressed = 0
        self.switch4_pressed = 0
        self.switch1_pos_angle = 0
        self.switch2_pos_angle = 0
        self.switch3_pos_angle = 0
        self.switch4_pos_angle = 0
        self.start()

    def execute(self, event):
        command = event['command']
        method = getattr(self, command, lambda x: print('Invalid'))
        method(event['value'])

    def motor1_set_angle(self, value):
        self.motor1_angle = (2*3.14 / 360 ) * value

    def switch1_set_pos_angle(self, value):
        self.switch1_pos_angle = (2*3.14 / 360 ) * value

    def switch1_set_pressed(self, value):
        self.switch1_pressed = value

    def switch2_set_pos_angle(self, value):
        self.switch2_pos_angle = (2*3.14 / 360 ) * value

    def switch2_set_pressed(self, value):
        self.switch2_pressed = value

    def switch3_set_pos_angle(self, value):
        self.switch3_pos_angle = (2*3.14 / 360 ) * value

    def switch3_set_pressed(self, value):
        self.switch3_pressed = value

    def switch4_set_pos_angle(self, value):
        self.switch4_pos_angle = (2*3.14 / 360 ) * value

    def switch4_set_pressed(self, value):
        self.switch4_pressed = value

    def run(self):
        while True:
            event = queue.get()
            self.execute(event)
            time.sleep(0.001)

    def event_loop(self):
        import arcade
        global queue

        try:
            width = conf.get_int(section="screen", key="width")
            height = conf.get_int(section="screen", key="height")
            center_x = width // 2
            center_y = height // 2
            switch_diameter =  conf.get_int(section="switch", key="diameter")

            # Start the render. This must happen before any drawing
            # commands. We do NOT need an stop render command.
            arcade.start_render()

            # Draw the outline of the radar
            arcade.draw_circle_filled(center_x, center_y, SWEEP_LENGTH,
                                       arcade.color.BALL_BLUE, 50)
            # Draw the radar line
            x = SWEEP_LENGTH * math.sin(self.motor1_angle) + center_x
            y = SWEEP_LENGTH * math.cos(self.motor1_angle) + center_y
            arcade.draw_line(center_x, center_x, x, y, arcade.color.OLIVE, 4)

            # draw endswitch1
            x = SWEEP_LENGTH * math.sin(self.switch1_pos_angle) + center_x
            y = SWEEP_LENGTH * math.cos(self.switch1_pos_angle) + center_y
            if self.switch1_pressed:
                arcade.draw_circle_filled(x, y, switch_diameter, arcade.color.BARBIE_PINK, 10)
            else:
                arcade.draw_circle_filled(x, y, switch_diameter, arcade.color.BLUE_GRAY, 10)

            # draw endswitch2
            x = SWEEP_LENGTH * math.sin(self.switch2_pos_angle) + center_x
            y = SWEEP_LENGTH * math.cos(self.switch2_pos_angle) + center_y
            if self.switch2_pressed:
                arcade.draw_circle_filled(x, y, switch_diameter, arcade.color.BARBIE_PINK,10)
            else:
                arcade.draw_circle_filled(x, y, switch_diameter, arcade.color.BLUE_GRAY,10)

        except Exception as ex:
            print(ex)

def execute(value):
    global queue
    queue.put(value)



def display(q):
    global queue
    global commander
    queue = q
    commander = Commander()

    import arcade
    try:
        # Open up our window
        arcade.open_window(conf.get_int(section="screen", key="width"), conf.get_int(section="screen", key="height"), "Gimbal Simulator")
        arcade.set_background_color(arcade.color.BLACK)

        # Tell the computer to call the draw command at the specified interval.
        arcade.schedule(lambda delta_time: commander.event_loop(), 1 / 80)

        # Run the program
        arcade.run()

        # When done running the program, close the window.
        arcade.close_window()
    except Exception as exc:
        print(exc)
        print("Error")
