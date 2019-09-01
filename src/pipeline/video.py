import cv2
import threading
import traceback
import os
import signal
import queue

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'X264')

class VideoRecorder:

    def __init__(self, queue_input, queue_output, queue_debug):

        self.queue_input = queue_input
        self.queue_output = queue_output
        self.queue_debug = queue_debug

        self.debug = False

        self.last_frames = queue.Queue()

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
                height, width, channels = image.shape
                self.queue_output.put((image, meta))

                self.last_frames.put(image)
                if self.last_frames.qsize() > 60:
                    out = cv2.VideoWriter('outpy.avi',fourcc, 10, (width,height))
                    try:
                        while True:
                            frame, meta = self.last_frames.get_nowait()
                            out.write(frame)
                    except:
                        pass
                    out.release()


                if self.debug:
                    self.queue_debug.put((image, meta))
            except:
                self.run_thread = False
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                os.kill(os.getpid(), signal.SIGTERM)
