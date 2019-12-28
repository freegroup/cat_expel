from file.configuration import Configuration
import sys
from pydoc import locate

conf = Configuration(inifile="config/service.ini")

from hal.axis import Axis

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
print("Using hardware layer :"+HARDWARE)
Hardware.Axis_horizontal = Axis(Hardware.Motor1, Hardware.Motor2, Hardware.Switch1, Hardware.Switch2)
Hardware.Axis_vertical = Axis(Hardware.Motor3, Hardware.Motor4, Hardware.Switch3, Hardware.Switch4)
