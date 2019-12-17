import cv2
import queue
import collections

from hal import Hardware

Hardware.Axis_vertical.off()
Hardware.Axis_horizontal.off()

while True:
    print(Hardware.Switch3.is_pressed())

cv2.destroyAllWindows()
