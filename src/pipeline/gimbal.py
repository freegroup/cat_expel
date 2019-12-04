import signal
import sys
import os
from hal import Hardware

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)


# Keep watching in a loop
def gimbal_adjust(context):

    try:
        angle_queue.put(filename)
        return True

    except:
        print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
        # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
        # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
        # SIGTERM event from outside.
        os.kill(os.getpid(), signal.SIGTERM)
