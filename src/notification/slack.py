import os
import slack
import threading
import signal
import time

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)

class Sender:
    def __init__(self, interval_seconds=60):
        self.run_thread = True
        self.sync_event = threading.Event()
        self.thread = threading.Thread(target=self.__run, args=())
        self.thread.daemon = True      # Daemonized thread
        self.thread.start()            # Start the execution
        self.interval_seconds = interval_seconds
        self.current_message = "msg"
        self.last_message_sent = time.time()-interval_seconds

    def __del__(self):
        self.run_thread = False

    def post_message(self, message, image=None):
        self.current_message = message
        self.sync_event.set()

    # Keep watching in a loop
    def __run(self):
        while self.run_thread:
            try:
                # Look for changes:
                # FileWatch didn't work. In Kubernetes "secrets" are memoryMapFiles. Therefore the timestamp
                # didn't change if you have already the filehandle. You MUST call always os.stat in a periodic way
                #
                self.sync_event.wait()

                # send only one message per "interval_seconds". Sleep for a while (message lost is possible)
                diff = (time.time() - self.last_message_sent)-self.interval_seconds
                if diff < 0:
                    time.sleep(-diff)

                client = slack.WebClient(token=conf.get("api_token", section="slack"))

                response = client.chat_postMessage(
                    channel='#allgemein',
                    text=self.current_message)
                assert response["ok"]
                self.sync_event.clear()
                self.last_message_sent = time.time()

            except (KeyboardInterrupt, SystemExit):
                self.run_thread = False
                # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
                # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
                # SIGTERM event from outside.
                os.kill(os.getpid(), signal.SIGTERM)
            except:
                print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
