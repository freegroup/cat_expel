import cv2
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

def detect():
    global lock, outputFrame

    images = get_image()
    for image in images:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        context.current_frame = image

        write_history(context)
        boxes, motion_frame = detect_motion(context, debug=True)
        if boxes is not None:
            prediction, detection_frame = detect_object(context, debug=True)
            if prediction is not None:
                slack_send(context)

        show_img = detection_frame

        scale_percent = 40 # percent of original size
        width = int(show_img.shape[1] * scale_percent / 100)
        height = int(show_img.shape[0] * scale_percent / 100)
        dim = (width, height)

        thumbnail = cv2.resize(show_img, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow("image", thumbnail)

detect()

cv2.destroyAllWindows()
