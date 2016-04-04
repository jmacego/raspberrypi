import gevent
from gevent.event import Event
import RPi.GPIO as GPIO                    #Import GPIO library
import sys, os
import time                                #Import time library

class hcsr04:
    """Class for interfaing with HC-SR04 ultrasonic distance sensors
    
    ***Be Aware: HC-SR04 is 5v so echo needs some help."""
    
    
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo    
        self.pulse_start = 0
        self.pulse_end = 0
        self.distance = 0
        
        GPIO.setup(self.trig,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(self.echo,GPIO.IN)                   #Set pin as GPIO in
        GPIO.output(self.trig, GPIO.LOW)
        GPIO.add_event_detect(self.echo, GPIO.BOTH, callback=self.__echo_interrupt)

    def send_trig(self):
        GPIO.output(self.trig, GPIO.HIGH)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(self.trig, GPIO.LOW)                 #Set TRIG as LOW
    
    def get_distance(self):
        return self.distance
        
    def __echo_interrupt(self, channel):
        if self.pulse_start == 0:
            self.pulse_start = time.time()              #Saves the last known time of LOW pulse
        else:
            self.pulse_end = time.time()                #Saves the last known time of HIGH pulse 
            print "Pulse Start: ", self.pulse_start
            print "Pulse End: ", self.pulse_end
            pulse_duration = self.pulse_end - self.pulse_start #Get pulse duration to a variable
            print "Pulse Duration: ", pulse_duration
            self.pulse_start = 0
            self.pulse_end = 0
            if pulse_duration < 0.025 :
                self.distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
                self.distance = round(self.distance, 2)            #Round to two decimal points

                if self.distance > 2 and self.distance < 400:      #Check whether the distance is within range
                    self.distance -= 0.5      #Print distance with 0.5 cm calibration
                else:
                    self.distance = -1                   #display out of range
            else:
                self.distance = -1