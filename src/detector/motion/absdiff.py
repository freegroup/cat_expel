import cv2
import numpy as np
import itertools

# my Rectangle = (x1, y1, x2, y2), a bit different from OP's x, y, w, h
def intersection(rectA, rectB): # check if rect A & B intersect
    a, b = rectA, rectB
    startX = max( min(a[0], a[2]), min(b[0], b[2]) )
    startY = max( min(a[1], a[3]), min(b[1], b[3]) )
    endX = min( max(a[0], a[2]), max(b[0], b[2]) )
    endY = min( max(a[1], a[3]), max(b[1], b[3]) )
    if startX < endX and startY < endY:
        return True
    else:
        return False

def combineRect(rectA, rectB): # create bounding box for rect A & B
    a, b = rectA, rectB
    startX = min( a[0], b[0] )
    startY = min( a[1], b[1] )
    endX = max( a[2], b[2] )
    endY = max( a[3], b[3] )
    return (startX, startY, endX, endY)

def checkIntersectAndCombine(rects):
    if rects is None:
        return None
    mainRects = rects
    noIntersect = False
    while noIntersect == False and len(mainRects) > 1:
        mainRects = list(set(mainRects))
        # get the unique list of rect, or the noIntersect will be
        # always true if there are same rect in mainRects
        newRectsArray = []
        for rectA, rectB in itertools.combinations(mainRects, 2):
            newRect = []
            if intersection(rectA, rectB):
                newRect = combineRect(rectA, rectB)
                newRectsArray.append(newRect)
                noIntersect = False
                # delete the used rect from mainRects
                if rectA in mainRects:
                    mainRects.remove(rectA)
                if rectB in mainRects:
                    mainRects.remove(rectB)
        if len(newRectsArray) == 0:
            # if no newRect is created = no rect in mainRect intersect
            noIntersect = True
        else:
            # loop again the combined rect and those remaining rect in mainRects
            mainRects = mainRects + newRectsArray
    return mainRects


__old_tested_image = None
def motion_detection(image):
    global __old_tested_image

    image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (15, 15), 0)

    if __old_tested_image is None:
        __old_tested_image = image
        return (__old_tested_image.copy(),[])

    delta = cv2.absdiff(__old_tested_image, image)

    _, delta = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3,3),np.uint8)
    delta = cv2.dilate(delta, kernel, iterations=3)

    cnts, _ = cv2.findContours(delta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for c in cnts:
        if cv2.contourArea(c) < 1000:
            continue
        objects.append(cv2.boundingRect(c))

    __old_tested_image = image

    return (__old_tested_image.copy(), checkIntersectAndCombine(objects))
