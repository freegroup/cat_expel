# Stel de GPIO pinnen in voor de stappenmotor:

import sys
import time
import RPi.GPIO as GPIO
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
pins = [23,24,25,4]
pin=4
 
# Set all pins as output
for p in pins:
    GPIO.setup(p,GPIO.OUT)
    GPIO.output(p, False)

while True:
  GPIO.output(pin, True)
  time.sleep(0.002)
  GPIO.output(pin, True)
  time.sleep(0.002)