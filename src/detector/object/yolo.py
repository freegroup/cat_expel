import cv2
import numpy as np
import os
from util import download_file
from detector.object.prediction import Prediction, Box
from enum import Enum

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_NAME = 'yolo'
PATH_TO_MODELS = os.path.join(CWD_PATH, "model")
PATH_TO_WEIGHTS = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'yolov3.weights')
PATH_TO_CFG = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'yolov3.cfg')
PATH_TO_CLASSES = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'yolov3.names')

def __download_model():
    url_weight= "https://pjreddie.com/media/files/yolov3.weights"
    url_cfg = "https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg?raw=true"
    url_names = "https://github.com/pjreddie/darknet/blob/master/data/coco.names?raw=true"

    fileAlreadyExists = os.path.isfile(PATH_TO_WEIGHTS)
    if not fileAlreadyExists:
        if not os.path.exists(os.path.join(PATH_TO_MODELS, MODEL_NAME)):
            os.makedirs(os.path.join(PATH_TO_MODELS, MODEL_NAME))
        print('Downloading frozen inference graph (.weight, .cfg, .classes): ')
        download_file(url_weight, PATH_TO_WEIGHTS)
        download_file(url_cfg, PATH_TO_CFG)
        download_file(url_names, PATH_TO_CLASSES)

__download_model()


net = cv2.dnn.readNet(PATH_TO_WEIGHTS, PATH_TO_CFG)


class predict_ids(Enum):
  PERSON =0
  TEDDY_BEAR=77
  CAT = 15
  DOG = 16


def predict(image, class_to_detect):
    scale = 0.00392
    image_height, image_width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    predictions = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == class_to_detect.value:
                center_x = int(detection[0] * image_width)
                center_y = int(detection[1] * image_height)
                w = int(detection[2] * image_width)
                h = int(detection[3] * image_height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]

        box = boxes[i]
        x = int(box[0])
        y = int(box[1])
        w = int(box[2])
        h = int(box[3])
        predictions.append(Prediction(class_id=class_ids[i],
                                      img_w = image_width,
                                      img_h=image_height,
                                      bounding_box=Box(x, y, w, h)))
    return predictions

