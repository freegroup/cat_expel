import os
import cv2
import time
import numpy as np
from multiprocessing import Process
from multiprocessing import Queue

from detector.object.prediction import Prediction, Box
import edgetpu.detection.engine
from edgetpu.utils import image_processing
from PIL import Image
from enum import Enum


CWD_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_NAME = 'coral'
PATH_TO_MODELS =os.path.join(CWD_PATH, "model")
PATH_TO_MODEL = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

engine = edgetpu.detection.engine.DetectionEngine(PATH_TO_MODEL)



class predict_ids(Enum):
  PERSON =0
  TEDDY_BEAR=87
  CAT = 16
  DOG = 17


def predict(image, class_to_detect, confidence):
    image_height, image_width= image.shape[:2]
    image = Image.fromarray(image)
    results = engine.DetectWithImage(image, threshold=0.4, keep_aspect_ratio=True, relative_coord=False, top_k=10)

    predictions = []

    if results:
        for obj in results:
            box = obj.bounding_box.flatten().tolist()
            xmin = int(box[0])
            ymin = int(box[1])
            xmax = int(box[2])
            ymax = int(box[3])
            if obj.score > confidence and obj.label_id == class_to_detect.value:
  
                predictions.append(Prediction(class_id=obj.label_id,
                                            img_w = image_width,
                                            img_h=image_height,
                                            bounding_box=Box(xmin, ymin, xmax-xmin, ymax-ymin)))
    return predictions

