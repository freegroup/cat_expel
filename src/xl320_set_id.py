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
port = "/dev/ttyS0"

old_id = 1
new_id = 3

serial = ServoSerial(port=port)
serial.open()

servo = Packet(servoType)

pkt = servo.makeWritePacket(old_id, servo.base.ID, [new_id])
serial.sendPkt(pkt)  # send packet to servo
    