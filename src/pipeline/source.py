import cv2

cap = cv2.VideoCapture(0)

def get_image():
    while True:
        # Capture frame-by-frame
        _, image = cap.read()

        if image is None:
            continue
        yield image
