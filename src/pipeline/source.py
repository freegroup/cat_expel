import cv2
import numpy as np
import time
import imutils

cap1 = cv2.VideoCapture(0)
time.sleep(3.0)
cap2 = cv2.VideoCapture(1)
time.sleep(3.0)

# initialize the video stream and allow the camera sensor to
# warmup
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

def get_image():
    while True:
        # Capture frame-by-frame
        ret1, image1 = cap1.read()
        ret2, image2 = cap2.read()

        if not ret1:
            continue

        if not ret2:
            continue


        #image1 = hisEqulColor(image1)
        #image2 = hisEqulColor(image2)

        (h, w) = image2.shape[:2]
        # calculate the center of the image
        center = (w / 2, h / 2)
        angle180 = 180
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle180, scale)
        image2 = cv2.warpAffine(image2, M, (w, h))

        #status, double = stitcher.stitch([image1, image2])
        #if status != cv2.Stitcher_OK:
        #    print("Can't stitch images, error code = %d" % status)
        #    yield np.concatenate((image1, image2), axis=1)
        #else:
        #    yield double
        yield np.concatenate((image1, image2), axis=1)

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def hisEqulColor(img):
    ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    channels=cv2.split(ycrcb)
    cv2.equalizeHist(channels[0],channels[0])
    cv2.merge(channels,ycrcb)
    cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
    return img
