import signal
import sys
import os
import math
from hal import Hardware

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)


# Keep watching in a loop
def gimbal_adjust(context):

    try:
        box = context.prediction.bounding_box
        img_w = context.prediction.img_w
        img_h = context.prediction.img_h
        center_of_box = (int((box.x+box.w)/2), int((box.y+box.h)/2))
        norm_x, norm_y = (int((box.x+box.w)/2)/img_w-0.5, int((box.y+box.h)/2)/img_h-0.5)
        radian = math.sin(norm_x)
        degree = math.degrees(radian)*2
        Hardware.Axis_x.set_target_angle(degree)

    except:
        print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
        # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
        # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
        # SIGTERM event from outside.
        os.kill(os.getpid(), signal.SIGTERM)
