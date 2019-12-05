from configparser import ConfigParser
import threading
import sys
import time
import os
import signal

def nop_callback():
    pass

class Configuration:

    def __init__(self, inifile=None, reload_on_change=False, after_reload_callback=None):
        if os.path.isfile(inifile) is False:
            print("unable to find configuration file [{}]".format(inifile), file=sys.stderr)
            sys.exit(1)

        self.after_reload_callback = after_reload_callback
        if self.after_reload_callback is None:
            self.after_reload_callback = nop_callback
        self.cached_stamp = None
        self.file = inifile
        self.config = ConfigParser()
        self.config.read(self.file)
        self.run_thread = False

        # Reload the configuration file if something has changed
        #
        if reload_on_change is True:
            self.run_thread = True
            self.thread = threading.Thread(target=self.__run, args=())
            self.thread.setDaemon(True)      # Daemonized thread
            self.thread.start()          # Start the execution

    def __del__(self):
        self.run_thread = False

    def get_boolean(self, key, section="common"):
        return (self.get(key, section)).lower() in ("y", "yes", "true", "t", "1")

    def get_int(self, key, section="common"):
        return int(self.get(key, section))

    def get(self, key, section="common"):
        try:
            return self.config[section][key]
        except KeyError:
            print("Unable to find key [{}] in ini file [{}]".format(key, self.file),  file=sys.stderr)
            sys.exit(1)

    def section(self, section="common"):
        return dict(self.config.items(section))

    # Keep watching in a loop
    def __run(self):
        while self.run_thread:
            try:
                # Look for changes:
                # FileWatch didn't work. In Kubernetes "secrets" are memoryMapFiles. Therefore the timestamp
                # didn't change if you have already the filehandle. You MUST call always os.stat in a periodic way
                #
                time.sleep(2)

                stamp = os.stat(self.file).st_mtime

                if stamp != self.cached_stamp:
                    self.cached_stamp = stamp
                    # File has changed, so do something...
                    print("Ini-File [{}] changed. Reload configuration.".format(self.file))
                    self.config.read(self.file)
                    self.after_reload_callback()
            except (KeyboardInterrupt, SystemExit):
                self.run_thread = False
                # because we are running within a thread, a normal "sys.exit(1)" didn't work. Process didn't terminate.
                # sys.exit(...) throws just an exception which isn'T catch by the main thread. Workaround: send an
                # SIGTERM event from outside.
                os.kill(os.getpid(), signal.SIGTERM)
            except Exception as exc:
                print(exc)
                print('Unhandled error: {}'.format( sys.exc_info()[1]), file=sys.stderr)
