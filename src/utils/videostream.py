# import the necessary packages
from threading import Thread
import cv2
import time


class VideoStream:
    def __init__(self, src, fps=10, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 1920)
        self.stream.set(4, 1080)
        # self.stream.set(cv2.CAP_PROP_FPS, 10)
        # cv2.SetCaptureProperty(self.stream,cv2.CV_CAP_PROP_FRAME_WIDTH, 1280)
        # cv2.SetCaptureProperty(self.stream,cv2.CV_CAP_PROP_FRAME_HEIGHT, 720)

        # the camera needs some time to warm up
        time.sleep(2.0)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.setDaemon(True)
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        if not self.grabbed:
            return None
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
