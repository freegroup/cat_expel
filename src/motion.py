import cv2
from detector.motion.absdiff import motion_detection
from notification.slack import Sender

cap = cv2.VideoCapture(0)
sender = Sender()

while True:
    # Capture frame-by-frame
    ret, image = cap.read()

    image, objects = motion_detection(image)

    if len(objects) > 0:
        sender.post_message("object move detected")

    for obj in objects:
        x, y, w, h = obj
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    cv2.imshow("object detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
