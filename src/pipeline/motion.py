import cv2
import numpy as np
import itertools

__last_frame = None

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

def combine(boxes):
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


# Keep watching in a loop
def motion_detect(context, debug=False):
    image = context.current_frame

    global __last_frame

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    if __last_frame is None:
        __last_frame = blur
        return [], __last_frame

    delta = cv2.absdiff(__last_frame, blur)

    _, delta = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    delta = cv2.dilate(delta, kernel, iterations=3)

    cnts, _ = cv2.findContours(delta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in cnts:
        if cv2.contourArea(c) < 500:
            continue
        boxes.append(cv2.boundingRect(c))

    __last_frame = blur
    boxes = combine(boxes)

    dbg = blur
    if debug:
        dbg = blur.copy()
        for obj in boxes:
            x, y, w, h = obj
            cv2.rectangle(dbg, (x, y), (x + w, y + h), (255, 0, 0), 1)

    if len(boxes) > 0:
        return boxes, dbg
    else:
        return [], dbg
