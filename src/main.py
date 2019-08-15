import cv2

#from detector.yolo import predict, predict_ids
from detector.ssd_mobilenet_v2 import predict, predict_ids

def draw_prediction(img, prediction):
    image_height, image_width, _ = img.shape
    image_center = (int(image_width/2), int(image_height/2))
    color = (255,0,0)
    box = prediction.bounding_box
    img_w = prediction.img_w
    img_h = prediction.img_h
    center = (int((box.x+box.w)/2), int((box.y+box.h)/2))
    center_normalized = (int((box.x+box.w)/2)/img_w-0.5, int((box.y+box.h)/2)/img_h-0.5)

    cv2.circle(image, center, 30, color)

    if center_normalized[0] > 0.05:
        cv2.arrowedLine(image, image_center, (image_center[0]-100, image_center[1]), color,2 )
    elif center_normalized[0] < -0.05:
        cv2.arrowedLine(image, image_center, (image_center[0]+100, image_center[1]), color,2 )
    if center_normalized[1] > 0.05:
        cv2.arrowedLine(image, image_center, (image_center[0], image_center[1]-100), color,2 )
    elif center_normalized[1] < -0.05:
        cv2.arrowedLine(image, image_center, (image_center[0], image_center[1]+100), color,2 )


print('Reading from webcam.')
#cap = cv2.VideoCapture(0)

index =0
while True:
    # Capture frame-by-frame
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

cv2.destroyAllWindows()
