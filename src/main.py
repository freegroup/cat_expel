import cv2
import queue
import collections

# just for video streaming
from flask import Response
from flask import Flask
from flask import render_template
import threading
import time
context = collections.namedtuple('Context', 'last_frame last_frames current_frame debug_frame')
context.last_frames = queue.Queue()
context.last_frame = None

from pipeline.slack import slack_send
from pipeline.motion import detect_motion
from pipeline.predict import detect_object
from pipeline.source import get_image
from pipeline.history import write_history

print('Reading from webcam.')

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")


def detect():
    global outputFrame

    # give flask some time to bootstrap the server
    time.sleep(0.02)

    images = get_image()
    for image in images:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.02)

        context.current_frame = image

        write_history(context)
        boxes, motion_frame = detect_motion(context, debug=True)
        if boxes is not None:
            prediction, detection_frame = detect_object(context, debug=True)
            if prediction is not None:
                slack_send(context)

        display = detection_frame
        scale_percent = 40 # percent of original size
        width = int(display.shape[1] * scale_percent / 100)
        height = int(display.shape[0] * scale_percent / 100)
        dim = (width, height)
        display = cv2.resize(display, dim, interpolation=cv2.INTER_AREA)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = display.copy()


# start a thread that will perform motion detection
t = threading.Thread(target=detect)
t.daemon = True
t.start()


# start the flask app
app.run(host="0.0.0.0", port="8080", debug=False,threaded=False, use_reloader=False)

cv2.destroyAllWindows()
