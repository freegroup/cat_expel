# Stel de GPIO pinnen in voor de stappenmotor:

import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

 #  Motor 1 = [17,18,27,22]
 #  Motor 2 = [23,24,25,4]
 #  Motor 3 = [13,12,6,5]
 #  Motor 4 = [20,26,16,19]
      
# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
  
class Motor:

    def __init__(self, pins):
      self.step_pins = pins

      # Set all pins as output
      for pin in self.step_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

      self.step_count = len(Seq)
      self.wait_time = 0.001
 
      # Initialise variables
      self.step_counter = 0
 
    def step(self, dir):
      # Start main loop
      for pin in range(0, 4):
        xpin = self.step_pins[pin]#
        if Seq[self.step_counter][pin]!=0:
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
    
      self.step_counter += dir
    
      # If we reach the end of the sequence
      # start again
      if (self.step_counter>=self.step_count):
        self.step_counter = 0
      if (self.step_counter<0):
        self.step_counter = self.step_count+dir
      time.sleep(self.wait_time)