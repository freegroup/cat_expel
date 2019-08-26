import os
import threading
import signal
import time
import sys
import cv2
import numpy as np
import itertools
import traceback

class MotionDetector:

    def __init__(self, image_provider):
        self.__detected_image = None
        self.__debug_image = None
        self.__last_tested_image = None

        self.image_provider = image_provider

        self.run_thread = True
        self.sync_event = threading.Event()
        self.thread = threading.Thread(target=self.__run, args=())
        self.thread.daemon = True      # Daemonized thread
        self.thread.start()            # Start the execution

    def __del__(self):
        self.run_thread = False


    def forwarding_image(self):
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
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (15, 15), 0)

                if self.__last_tested_image is None:
                    self.__last_tested_image = blur
                    continue

                delta = cv2.absdiff(self.__last_tested_image, blur)

                _, delta = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)

                kernel = np.ones((3,3),np.uint8)
                delta = cv2.dilate(delta, kernel, iterations=3)

                cnts, _ = cv2.findContours(delta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                objects = []
                for c in cnts:
                    if cv2.contourArea(c) < 500:
                        continue
                    objects.append(cv2.boundingRect(c))

                self.__last_tested_image = blur
                objects = self.combine(objects)

                if len(objects) > 0:
                    self.__detected_image = image
                    self.__debug_image = image.copy()
                    for obj in objects:
                        x, y, w, h = obj
                        cv2.rectangle(self.__debug_image, (x, y), (x + w, y + h), (255, 0, 0), 1)

            except:
                self.run_thread = False
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                os.kill(os.getpid(), signal.SIGTERM)

    def combine(self, rects):
        if rects is None:
            return None

        main_rects = rects
        no_intersect = False
        while no_intersect == False and len(main_rects) > 1:
            main_rects = list(set(main_rects))
            # get the unique list of rect, or the noIntersect will be
            # always true if there are same rect in mainRects
            new_rects_array = []
            for rectA, rectB in itertools.combinations(main_rects, 2):
                if self.intersection(rectA, rectB):
                    new_rect = self.combine_rect(rectA, rectB)
                    new_rects_array.append(new_rect)
                    no_intersect = False
                    # delete the used rect from mainRects
                    if rectA in main_rects:
                        main_rects.remove(rectA)
                    if rectB in main_rects:
                        main_rects.remove(rectB)
            if len(new_rects_array) == 0:
                # if no newRect is created = no rect in mainRect intersect
                no_intersect = True
            else:
                # loop again the combined rect and those remaining rect in mainRects
                main_rects = main_rects + new_rects_array
        return main_rects

    # my Rectangle = (x1, y1, x2, y2), a bit different from OP's x, y, w, h
    def intersection(self, rectA, rectB): # check if rect A & B intersect
        a, b = rectA, rectB
        startX = max( min(a[0], a[2]), min(b[0], b[2]) )
        startY = max( min(a[1], a[3]), min(b[1], b[3]) )
        endX = min( max(a[0], a[2]), max(b[0], b[2]) )
        endY = min( max(a[1], a[3]), max(b[1], b[3]) )
        if startX < endX and startY < endY:
            return True
        else:
            return False

    def combine_rect(self, rectA, rectB): # create bounding box for rect A & B
        a, b = rectA, rectB
        startX = min( a[0], b[0] )
        startY = min( a[1], b[1] )
        endX = max( a[2], b[2] )
        endY = max( a[3], b[3] )
        return (startX, startY, endX, endY)
