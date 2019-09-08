import os
import slack
import threading
import signal
import time
import sys
import cv2

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)

class Sender:
    def __init__(self, queue_input, queue_output, queue_debug):
        self.queue_input = queue_input
        self.queue_output = queue_output
        self.queue_debug = queue_debug

        self.debug = False

        self.interval_seconds = conf.get_int("interval_seconds", section="slack")
        self.last_message_sent = time.time()-self.interval_seconds

        self.run_thread = True
        self.thread = threading.Thread(target=self.__run, args=())
        self.thread.daemon = True      # Daemonized thread
        self.thread.start()            # Start the execution


    def __del__(self):
        self.run_thread = False

    # Keep watching in a loop
    def __run(self):
        while self.run_thread:
            try:
                image, meta = self.queue_input.get()
                # send only one message per "interval_seconds". Sleep for a while (message lost is possible)
                diff = (time.time() - self.last_message_sent)-self.interval_seconds
                if diff < 0:
                    continue

                cv2.imwrite("test.png", image)
                client = slack.WebClient(token=conf.get("api_token", section="slack"))
                client.files_upload(
                    channels="#allgemein",
                    file="test.png",
                    title="Target detected"
                )
                if self.debug:
                    self.queue_debug.put((image, None))

                self.last_message_sent = time.time()
            except:
                print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
                self.run_thread = False
                # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
                # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
                # SIGTERM event from outside.
                os.kill(os.getpid(), signal.SIGTERM)
