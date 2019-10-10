import cv2
import numpy as np
import time
import sys

from utils.videostream import VideoStream
from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)
fps = conf.get_int("fps", section="camera")

#cap1 = VideoStream("/dev/v4l/by-id/usb-046d_081b_539A4A60-video-index0")
cap1 = VideoStream("/dev/video0")
cap1.start()
#cap1.set(cv2.CAP_PROP_FPS, fps)

#cap2 = VideoStream("/dev/v4l/by-id/usb-046d_081b_57618940-video-index0")
cap2 = VideoStream("/dev/video2")
cap2.start()
#cap2.set(cv2.CAP_PROP_FPS, fps)

def get_image():
    time.sleep(5)
    while True:
        try:

            # Capture frame-by-frame
            image1 = None #cap1.read()
            image2 = None #cap2.read()

            if image1 is None:
                continue

            if image2 is None:
                continue
            print("blubber")
            (h, w) = image2.shape[:2]
            # calculate the center of the image
            center = (w / 2, h / 2)
            angle180 = 180
            scale = 1.0
            M = cv2.getRotationMatrix2D(center, angle180, scale)
            image2 = cv2.warpAffine(image2, M, (w, h))

              
            yield np.concatenate((image1, image2), axis=1)
            print("image_readed")
        except:
            print("error....")
