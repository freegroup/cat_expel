import cv2

#from detector.object.yolo import predict, predict_ids
# from detector.object.ssd_mobilenet_v2 import predict, predict_ids
from detector.object.coral import predict, predict_ids


# Keep watching in a loop
def object_detect(context, debug=False):
    image = context.current_frame

    predictions = predict(image, predict_ids.PERSON, 0.4)
    dbg = image
    if debug:
        dbg = image.copy()
        for p in predictions:
            draw_prediction(dbg, p)

    if len(predictions) > 0:
        context.prediction = predictions[0]
        return predictions, dbg
    else:
        context.prediction = None
        return None, dbg


def draw_prediction(img, prediction):
    image_height, image_width, _ = img.shape
    color = (0,0,250)
    box = prediction.bounding_box
    center = (int(box.x+(box.w/2)), int(box.y+(box.h/2)))
    print(image_width, image_height, box, center)
    cv2.circle(img, center, 30, color, thickness=5)
    cv2.rectangle(img, box, color, thickness=2) 
