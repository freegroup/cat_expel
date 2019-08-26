import cv2
import time
from notification.slack import Sender
from pipeline.image_cache import ImageCache
from pipeline.motion import MotionDetector
from pipeline.predict import ObjectDetector

print('Reading from webcam.')


cap = cv2.VideoCapture(0)

cache = ImageCache()
motion = MotionDetector(cache)
predict = ObjectDetector(motion)

sender = Sender()

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Capture frame-by-frame
    ret, image = cap.read()

    cache.push(image)

    # Required. Otherwise the GIL won't scheduled the other threads
    time.sleep(0.05)

    if predict.debug_image() is not None:
        cv2.imshow("object detection", predict.debug_image())


#        if len(predictions) > 0:
#            sender.post_message("object move detected", image)

cap.release()
cv2.destroyAllWindows()
