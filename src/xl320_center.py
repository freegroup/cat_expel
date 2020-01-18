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
port = "/dev/ttyS0"

angle = 30
speed= 312

serial = ServoSerial(port=port)
serial.open()

servo = Packet(servoType)
def set_angle(id, angle):
    val = angle2int(angle, degrees=True) + le(speed)
    pkt = servo.makeWritePacket(id, servo.base.GOAL_POSITION, val)
    serial.sendPkt(pkt)  # send packet to servo

while True:
    set_angle(1,150)
    set_angle(2,150)
    set_angle(3,150)
    set_angle(4,150)
time.sleep(2)
    