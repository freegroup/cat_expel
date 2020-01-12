import math
from hal import Hardware

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini")

def gimbal_adjust(context):
    box = context.prediction.bounding_box
    img_w = context.prediction.img_w
    img_h = context.prediction.img_h

    x, y = (int(box.x+(box.w/2)), int(box.y+(box.h/2)))
    norm_x, norm_y =(x/img_w-0.5, y/img_h-0.5)

    radian = -math.sin(norm_x)
    degree = math.degrees(radian)*1.8
    Hardware.Axis_horizontal.set_angle(degree)
    return

    radian = -math.sin(norm_y)
    degree = math.degrees(radian)*1.4
    Hardware.Axis_vertical.set_angle(degree)
