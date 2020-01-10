from pyservos import Packet
from pyservos.servoserial import ServoSerial
import pyservos
from pyservos.utils import angle2int, le
import time

servoType = pyservos.XL320
servoStr =  'XL-320'
port = "/dev/ttyS0"
speed= 312

serial = ServoSerial(port=port)
serial.open()
servo = Packet(servoType)

class Motor:

    def __init__(self, id, inverse=False):
        self.id = id
        self.inverse = inverse
        self.angle = 0

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
        val = angle2int(angle, degrees=True) + le(speed)
        pkt = servo.makeWritePacket(self.id, servo.base.GOAL_POSITION, val)
        serial.sendPkt(pkt)  # send packet to servo
