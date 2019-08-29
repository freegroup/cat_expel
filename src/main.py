import cv2
import time
import queue
from notification.slack import Sender
from pipeline.motion import MotionDetector
from pipeline.predict import ObjectDetector

print('Reading from webcam.')


images_from_cam = queue.Queue(20)
images_from_motion = queue.Queue(20)
images_from_predict = queue.Queue(20)
images_to_show = queue.Queue(20)

cap = cv2.VideoCapture(0)


motion  = MotionDetector(images_from_cam, images_from_motion, images_to_show)
predict = ObjectDetector(images_from_motion, images_from_predict, images_to_show)

sender = Sender()

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capture frame-by-frame
    _, image = cap.read()

    if images_from_cam.full():
        images_from_cam.get_nowait()

    images_from_cam.put((image, None))

    # Required. Otherwise the GIL won't scheduled the other threads
    time.sleep(0.01)

    try:
        while True:
            dbg, meta = images_to_show.get_nowait()
            cv2.imshow("object detection", dbg)
    except:
        pass

    try:
        while True:
            images_from_motion.get_nowait()
    except:
        pass

#        if len(predictions) > 0:
#            sender.post_message("object move detected", image)

cap.release()
cv2.destroyAllWindows()
