import RPi.GPIO as GPIO                    #Import GPIO library
import sys, os
import time                                #Import time library

class hcsr04:
    """Class for interfaing with HC-SR04 ultrasonic distance sensors
    
    ***Be Aware: HC-SR04 is 5v so echo needs some help."""
    
    
    def __init__(self, trig, echo, AsyncResult):
        self.trig = trig
        self.echo = echo    
        self.pulse_start = 0
        self.pulse_end = 0
        self.distance = 0
        self.AsyncResult = AsyncResult
        
        GPIO.setup(self.trig,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(self.echo,GPIO.IN)                   #Set pin as GPIO in
        GPIO.output(self.trig, GPIO.LOW)
        GPIO.add_event_detect(self.echo, GPIO.BOTH, callback=self.__echo_interrupt)

    def send_trig(self):
        GPIO.output(self.trig, GPIO.HIGH)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(self.trig, GPIO.LOW)                 #Set TRIG as LOW
    
    def __echo_interrupt(self, channel):
        if self.pulse_start == 0:
            self.pulse_start = time.time()              #Saves the last known time of LOW pulse
        else:
            self.pulse_end = time.time()                #Saves the last known time of HIGH pulse 
            self.AsyncResult.set(self.pulse_end - self.pulse_start)
            self.pulse_start = 0
            self.pulse_end = 0
