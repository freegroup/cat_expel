import os
import signal
import sys
import cv2
import traceback

#from detector.object.yolo import predict, predict_ids
from detector.object.ssd_mobilenet_v2 import predict, predict_ids
#from detector.object.coral import predict, predict_ids


# Keep watching in a loop
def detect_object(context, debug=False):

    try:
        image = context.current_frame

        predictions = predict(image, predict_ids.PERSON, 0.4)
        dbg = image
        if debug:
            dbg = image.copy()
            for p in predictions:
                draw_prediction(dbg, p)

        if len(predictions) > 0:
            return predictions, dbg
        else:
            return None, dbg

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        os.kill(os.getpid(), signal.SIGTERM)

def draw_prediction(img, prediction):
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

