import os
import threading
import signal
import time
import sys
import cv2
import traceback

#from detector.object.yolo import predict, predict_ids
from detector.object.ssd_mobilenet_v2 import predict, predict_ids

class ObjectDetector:

    def __init__(self, image_provider):
        self.__detected_image = None
        self.__debug_image = None
        self.image_provider = image_provider

        self.run_thread = True
        self.sync_event = threading.Event()
        self.thread = threading.Thread(target=self.__run, args=())
        self.thread.daemon = True      # Daemonized thread
        self.thread.start()            # Start the execution

    def __del__(self):
        self.run_thread = False

    def detected_image(self):
        return self.__detected_image

    def debug_image(self):
        return self.__debug_image

    # Keep watching in a loop
    def __run(self):
        while self.run_thread:
            try:
                image = self.image_provider.forwarding_image()
                if image is None:
                    time.sleep(0.1)
                    continue

                image = image.copy()
                predictions = predict(image, predict_ids.PERSON)
                if len(predictions) > 0:
                    self.__detected_image = image
                    tmp = image.copy()
                    for p in predictions:
                        self.draw_prediction(tmp, p)
                    self.__debug_image = tmp

            except:
                self.run_thread = False
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                os.kill(os.getpid(), signal.SIGTERM)

    def draw_prediction(self, img, prediction):
        image_height, image_width, _ = img.shape
        image_center = (int(image_width/2), int(image_height/2))
        color = (0,0,250)
        box = prediction.bounding_box
        img_w = prediction.img_w
        img_h = prediction.img_h
        center = (int((box.x+box.w)/2), int((box.y+box.h)/2))
        center_normalized = (int((box.x+box.w)/2)/img_w-0.5, int((box.y+box.h)/2)/img_h-0.5)

        cv2.circle(img, center, 30, color, thickness=5)

    #    if center_normalized[0] > 0.05:
    #        cv2.arrowedLine(image, image_center, (image_center[0]-100, image_center[1]), color,2 )
    #    elif center_normalized[0] < -0.05:
    #        cv2.arrowedLine(image, image_center, (image_center[0]+100, image_center[1]), color,2 )
    #    if center_normalized[1] > 0.05:
    #        cv2.arrowedLine(image, image_center, (image_center[0], image_center[1]-100), color,2 )
    #    elif center_normalized[1] < -0.05:
    #        cv2.arrowedLine(image, image_center, (image_center[0], image_center[1]+100), color,2 )

