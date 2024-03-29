import os
import signal
import time
import sys
import cv2
import queue
import traceback
import imageio
import threading
import telegram
from datetime import datetime, date

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)

bot = telegram.Bot(token=conf.get(section="telegram", key='api_token'))
chat_id = conf.get_int(section="telegram", key="channel_id")

interval_seconds = conf.get_int("interval_seconds", section="telegram")
last_message_sent = time.time()-interval_seconds
upload_queue = queue.Queue()


# Keep watching in a loop
def messanger_send(context):
    enabled = conf.get_boolean("enabled", section="telegram")
    if not enabled:
        return

    interval_seconds = conf.get_int("interval_seconds", section="telegram")
    global last_message_sent
    try:
        # send only one message per "interval_seconds". Sleep for a while (message lost is possible)
        diff = (time.time() - last_message_sent)-interval_seconds
        if diff < 0:
            return False

        filename = str(time.time())+".avi"
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
        try:
            last_frames = context.last_frames
            while True:
                frame = last_frames.get_nowait()
                scale_percent = 80 # percent of original size
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                resized = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
                # write the flipped frame
                out.write(resized)
        except queue.Empty:
            pass
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        out.release()
        upload_queue.put(filename)
        last_message_sent = time.time()
        return True

    except Exception as exc:
        print(exc)
        print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
        # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
        # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
        # SIGTERM event from outside.
        os.kill(os.getpid(), signal.SIGTERM)


# Keep watching in a loop
def run():
    global upload_queue
    bot = telegram.Bot(token=conf.get(section="telegram", key='api_token'))
    chat_id = conf.get_int(section="telegram", key="channel_id")

    while True:
        try:
            filename = upload_queue.get()
            print("Upload file '{}' to telegram".format(filename))
            bot.send_video(chat_id=chat_id, video=open(filename, 'rb'), supports_streaming=True, timeout=10000)
            os.remove(filename)
        except Exception as exc:
            # because we are running within a thread, q normal "sys.exit(1)" didn't work. Process didn't terminate.
            # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
            # SIGTERM event from outside.
            print(exc)
            print('Unhandled error: {}'.format( sys.exc_info()[1]))



thread = threading.Thread(target=run, args=())
thread.setDaemon(True)    # Daemonized thread
thread.start()            # Start the execution
