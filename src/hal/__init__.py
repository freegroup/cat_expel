from file.configuration import Configuration
import sys
from pydoc import locate

conf = Configuration(inifile="config/service.ini")


# Read the kind of input source from"service.ini" file and create an instance of them.
#
HARDWARE = conf.get('impl', 'hal')
if HARDWARE is None:
    print("No data source configured")
    sys.exit(1)
# create a python object by class name
Hardware = locate(HARDWARE)
if Hardware is None:
    print("Class [{}] not found.".format(HARDWARE))
    sys.exit(1)
