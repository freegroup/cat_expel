import cv2
import numpy as np

from utils.videostream import VideoStream
from file.configuration import Configuration


CWD_PATH = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(CWD_PATH, "hardware.ini"))


class Camera:
    def __init__(self):
        self.cap1 = VideoStream(conf.get(key="camera1", section="camera"))
        self.cap1.start()

        self.cap2 = VideoStream(conf.get(key="camera2", section="camera"))
        self.cap2.start()

    def read(self):
        # Capture frame-by-frame
        image1 = self.cap1.read()
        image2 = self.cap2.read()

        if image1 is None:
            return None

        if image2 is None:
            return None

        (h, w) = image2.shape[:2]
        # calculate the center of the image
        center = (w / 2, h / 2)
        angle180 = 180
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle180, scale)
        image2 = cv2.warpAffine(image2, M, (w, h))

        return np.concatenate((image1, image2), axis=1)
