import os
import cv2
from utils.videostream import VideoStream
from file.configuration import Configuration

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(CWD_PATH, "hardware.ini"))


class Camera:

    def __init__(self):
        self.cap = VideoStream(0)
        self.cap.start()

    def read(self):
        # Capture frame-by-frame
        image = self.cap.read()

        (h, w) = image.shape[:2]
        # calculate the center of the image
        center = (w / 2, h / 2)
        angle180 = 180
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle180, scale)
        return cv2.warpAffine(image, M, (w, h))
