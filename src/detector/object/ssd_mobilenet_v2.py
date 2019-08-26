import cv2
import os
import zipfile
from detector.object.prediction import Prediction, Box
from enum import Enum

CWD_PATH = os.path.dirname(os.path.realpath(__file__))

MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
PATH_TO_MODELS =os.path.join(CWD_PATH, "model")
PATH_TO_CKPT = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_PBTXT = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'graph.pbtxt')
PATH_TO_ZIP = os.path.join(PATH_TO_MODELS, MODEL_NAME+".zip")

def __prepare_model():
    fileAlreadyExists = os.path.isfile(PATH_TO_CKPT)
    if not fileAlreadyExists:
        print("Extract model.")
        if not os.path.exists(PATH_TO_MODELS):
            os.makedirs(PATH_TO_MODELS)
        zip_ref = zipfile.ZipFile(PATH_TO_ZIP, 'r')
        zip_ref.extractall(PATH_TO_MODELS)
        zip_ref.close()

__prepare_model()

# Pretrained classes in the model
#  0: 'background',
#  1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
#  7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
#  13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
#  18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
#  24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
#  32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
#  37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
#  41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
#  46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
#  51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
#  56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
#  61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
#  67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
#  75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
#  80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
#  86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'
class predict_ids(Enum):
    PERSON = 1
    TEDDY_BEAR= 88
    CAT = 17
    DOG = 18


# Loading model
print('Loading Model.')
model = cv2.dnn.readNetFromTensorflow(PATH_TO_CKPT, PATH_TO_PBTXT)


def predict(image, class_to_detect):
    image_height, image_width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, size=(300,300), swapRB=True)
    model.setInput(blob)
    output = model.forward()

    predictions = []
    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        class_id = detection[1]
        if confidence > .2 and class_id == class_to_detect.value:
            box_x = int(detection[3] * image_width)
            box_y = int(detection[4] * image_height)
            box_width = int(detection[5] * image_width)
            box_height = int(detection[6] * image_height)
            predictions.append(Prediction(class_id=class_id,
                                          img_h=image_height,
                                          img_w=image_width,
                                          bounding_box=Box(box_x, box_y, box_width, box_height)))
    return predictions
