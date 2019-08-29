import os
import threading
import signal
import sys
import cv2
import numpy as np
import itertools
import traceback

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return () # or (0,0,0,0) ?
    return (x, y, w, h)

class MotionDetector:

    def __init__(self, queue_input, queue_output, queue_debug):
        self.__last_tested_image = None

        self.queue_input = queue_input
        self.queue_output = queue_output
        self.queue_debug = queue_debug

        self.debug = False

        self.run_thread = True
        self.thread = threading.Thread(target=self.__run, args=())
        self.thread.daemon = True      # Daemonized thread
        self.thread.start()            # Start the execution

    def __del__(self):
        self.run_thread = False

    # Keep watching in a loop
    def __run(self):
        while self.run_thread:
            try:
                image, meta = self.queue_input.get()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (15, 15), 0)

                if self.__last_tested_image is None:
                    self.__last_tested_image = blur
                    continue

                delta = cv2.absdiff(self.__last_tested_image, blur)

                _, delta = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)

                kernel = np.ones((3, 3), np.uint8)
                delta = cv2.dilate(delta, kernel, iterations=3)

                cnts, _ = cv2.findContours(delta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                boxes = []
                for c in cnts:
                    if cv2.contourArea(c) < 500:
                        continue
                    boxes.append(cv2.boundingRect(c))

                self.__last_tested_image = blur
                boxes = self.combine(boxes)

                if len(boxes) > 0:
                    self.queue_output.put((image, boxes))

                if self.debug:
                    dbg = blur.copy()
                    for obj in boxes:
                        x, y, w, h = obj
                        cv2.rectangle(dbg, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    self.queue_debug.put((dbg, boxes))

            except:
                self.run_thread = False
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                os.kill(os.getpid(), signal.SIGTERM)

    def combine(self, boxes):
        # see https://stackoverflow.com/questions/21303374/example-for-opencv-grouprectangle-in-python before remove
        # the double line!
        double = boxes.copy()
        boxes.extend(double)
        boxes, weights =cv2.groupRectangles(boxes, 1)
        if type(boxes) is tuple:
            return []
        boxes = boxes.tolist()
        while True:
            found = 0
            for ra, rb in itertools.combinations(boxes, 2):
                if intersection(ra, rb):
                    if ra in boxes:
                        boxes.remove(ra)
                    if rb in boxes:
                        boxes.remove(rb)
                    boxes.append((union(ra, rb)))
                    found = 1
                    break
            if found == 0:
                break

        return boxes
