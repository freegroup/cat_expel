import cv2
import numpy as np
import time

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

# initialize the video stream and allow the camera sensor to
# warmup
time.sleep(2.0)

def get_image():
    while True:
        # Capture frame-by-frame
        _, image1 = cap1.read()
        _, image2 = cap2.read()

        if image1 is None:
            continue

        if image2 is None:
            continue

        double = np.concatenate((image1, image2), axis=1)

        yield double
