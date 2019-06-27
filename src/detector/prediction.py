from typing import NamedTuple

class Box(NamedTuple):
    x: int
    y: int
    w: int
    h: int

class Prediction(NamedTuple):
    img_w: int
    img_h: int
    bounding_box: Box
    class_id: int

