import cv2
import time
import queue
import collections

context = collections.namedtuple('Context', 'last_frame last_frames current_frame debug_frame')
context.last_frames = queue.Queue()
context.last_frame = None

from pipeline.slack import slack_send
from pipeline.motion import detect_motion
from pipeline.predict import detect_object
from pipeline.source import get_image
from pipeline.history import write_history

print('Reading from webcam.')

images = get_image()
for image in images:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    context.current_frame = image

    write_history(context)
    boxes = detect_motion(context)
    if boxes is not None:
        prediction = detect_object(context)
        if prediction is not None:
            slack_send(context)


    try:
        if context.debug_frame is not None:
            cv2.imshow("object detection", context.debug_frame)
        context.debug_frame = None
    except:
        pass


cv2.destroyAllWindows()
