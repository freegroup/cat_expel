import os
import slack
import signal
import time
import sys
import cv2
import queue
import traceback
import imageio
import threading
import os

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)


interval_seconds = conf.get_int("interval_seconds", section="slack")
last_message_sent = time.time()-interval_seconds
upload_queue = queue.Queue()


# Keep watching in a loop
def slack_send(context):
    global interval_seconds
    global last_message_sent
    try:
        # send only one message per "interval_seconds". Sleep for a while (message lost is possible)
        diff = (time.time() - last_message_sent)-interval_seconds
        if diff < 0:
            return False

        filename = str(time.time())+".gif"
        with imageio.get_writer(filename, mode='I') as writer:
            try:
                last_frames = context.last_frames
                while True:
                    frame = last_frames.get_nowait()
                    scale_percent = 20 # percent of original size
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    resized = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
                    writer.append_data(resized)
            except queue.Empty:
                pass
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

        upload_queue.put(filename)
        last_message_sent = time.time()
        return True

    except:
        print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
        # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
        # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
        # SIGTERM event from outside.
        os.kill(os.getpid(), signal.SIGTERM)


# Keep watching in a loop
def run():
    global upload_queue
    while True:
        try:
            filename = upload_queue.get()
            client = slack.WebClient(token=conf.get("api_token", section="slack"))
            client.files_upload(
                channels="#allgemein",
                file=filename,
                title="Target detected"
            )
            os.remove(filename)
        except:
            # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
            # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
            # SIGTERM event from outside.
            print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
            os.kill(os.getpid(), signal.SIGTERM)


thread = threading.Thread(target=run, args=())
thread.daemon = True      # Daemonized thread
thread.start()            # Start the execution
