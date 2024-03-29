import cv2
import queue
import collections

from hal import Hardware
# from pipeline.slack import messanger_send
from pipeline.telegram import messanger_send
from pipeline.motion import motion_detect
from pipeline.predict import object_detect
from pipeline.source import source_get_images
from pipeline.history import write_history
from pipeline.gimbal import gimbal_adjust

context = collections.namedtuple('Context', 'last_frame last_frames current_frame debug_frame prediction')
context.last_frames = queue.Queue()
context.last_frame = None

def detect():
    for image in source_get_images():
        try:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            context.current_frame = image

            show_img = image
            write_history(context)
            boxes, motion_frame = motion_detect(context, debug=True)
            if boxes is not None:
                prediction, detection_frame = object_detect(context, debug=True)
                if prediction is not None:
                    messanger_send(context)
                    gimbal_adjust(context)

                    show_img = detection_frame

            scale_percent = 40 # percent of original size
            width = int(show_img.shape[1] * scale_percent / 100)
            height = int(show_img.shape[0] * scale_percent / 100)
            dim = (width, height)

            thumbnail = cv2.resize(show_img, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow("image", thumbnail)
        except Exception as exc:
            print(exc)

Hardware.Axis_vertical.center()
Hardware.Axis_horizontal.center()

detect()

Hardware.Axis_vertical.off()
Hardware.Axis_horizontal.off()

cv2.destroyAllWindows()
