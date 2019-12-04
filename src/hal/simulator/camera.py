import os

from utils.videostream import VideoStream
from file.configuration import Configuration

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(CWD_PATH, "hardware.ini"))


class Camera:

    def __init__(self):
        self.cap = VideoStream(0)
        self.cap.start()
        pass

    def read(self):
        # Capture frame-by-frame
        return self.cap.read()
