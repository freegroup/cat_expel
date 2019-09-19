import cv2
import numpy as np
import time
import imutils
import threading

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)
fps = conf.get_int("fps", section="camera")

current_image = None
lock = threading.Lock()

cap1 = cv2.VideoCapture(2)
cap1.set(cv2.CAP_PROP_FPS, fps)
time.sleep(3.0)

cap2 = cv2.VideoCapture(0)
cap2.set(cv2.CAP_PROP_FPS, fps)
time.sleep(3.0)

# initialize the video stream and allow the camera sensor to
# warmup
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

def get_image():
    image = None
    while True:
        if(current_image is None):
            time.sleep(0.05)
            continue
        with lock:
            image = current_image.copy()
        print("image provided")
        yield image

# Keep watching in a loop
def __run():
    global current_image
    while run_thread:
        time.sleep(0.01)
        # Capture frame-by-frame
        ret1, image1 = cap1.read()
        ret2, image2 = cap2.read()

        if not ret1:
            continue

        if not ret2:
            continue

        (h, w) = image2.shape[:2]
        # calculate the center of the image
        center = (w / 2, h / 2)
        angle180 = 180
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle180, scale)
        image2 = cv2.warpAffine(image2, M, (w, h))

        with lock:
            current_image = np.concatenate((image1, image2), axis=1)
            print("image_readed")


run_thread = True
thread = threading.Thread(target=__run, args=())
thread.daemon = True      # Daemonized thread
thread.start()            # Start the execution
