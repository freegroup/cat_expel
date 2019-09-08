import cv2
import time
import queue

from pipeline.video import VideoRecorder
from pipeline.slack import Sender
from pipeline.motion import MotionDetector
from pipeline.predict import ObjectDetector

print('Reading from webcam.')


images_from_cam = queue.Queue(20)
images_from_recorder = queue.Queue(20)
images_from_motion = queue.Queue(20)
images_from_predict = queue.Queue(20)
images_to_show = queue.Queue(20)

cap = cv2.VideoCapture(0)

recorder = VideoRecorder(images_from_cam, images_from_recorder, images_to_show)
motion = MotionDetector(images_from_recorder, images_from_motion, images_to_show)
predict = ObjectDetector(images_from_motion, images_from_predict, images_to_show)
sender = Sender(images_from_predict, None, images_to_show)

index =0
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capture frame-by-frame
<<<<<<< HEAD
    cap = cv2.VideoCapture(index)
    ret, image = cap.read()
    cap.release()

    #image = cv2.flip( image, 0 )

    predictions = predict(image, predict_ids.CAT)
    for p in predictions:
        draw_prediction(image, p)

    cv2.imshow("object detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    index = (index+1)%2
=======
    _, image = cap.read()

    if images_from_cam.full():
        images_from_cam.get_nowait()
        continue

    images_from_cam.put((image, None))

    # Required. Otherwise the GIL won't scheduled the other threads
    time.sleep(0.05)

    try:
        dbg, meta = images_to_show.get_nowait()
        cv2.imshow("object detection", dbg)
    except:
        pass
>>>>>>> 9c764cd128a191b34c0871e0cf3fc4aa04c75e73

cap.release()
cv2.destroyAllWindows()
