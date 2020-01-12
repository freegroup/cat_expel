#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from pyservos import Packet
from pyservos.servoserial import ServoSerial
import pyservos
from pyservos.utils import angle2int, le
import time


servoType = pyservos.XL320
servoStr =  'XL-320'
ID= 1
port = "/dev/ttyS0"

angle = 30
speed= 312

print('Setting {} servo[{}] to {:.2f} on port {}'.format(servoStr, ID, angle, port))

serial = ServoSerial(port=port)
serial.open()

servo = Packet(servoType)
def set_angle(angle):
    val = angle2int(angle, degrees=True) + le(speed)
    pkt = servo.makeWritePacket(ID, servo.base.GOAL_POSITION, val)
    serial.sendPkt(pkt)  # send packet to servo

set_angle(150)
time.sleep(2)
    