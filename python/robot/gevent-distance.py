from gevent import monkey
monkey.patch_all()
import gevent
import RPi.GPIO as GPIO                    #Import GPIO library
import sys, os
import time                                #Import time library
from hcsr04 import hcsr04

distance_result = gevent.event.AsyncResult()

    
def main():
    GPIO.setmode(GPIO.BCM)
    gevent.joinall([
        gevent.spawn(trigger),
    ], timeout = 20)

    GPIO.cleanup()

def trigger():
    sensor = hcsr04(12, 16, distance_result)
    while True:
        sensor.send_trig();
        gevent.sleep(.1)
        pulse_duration = distance_result.get()
        if pulse_duration < 0.025 :
            distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
            distance = round(distance, 2)            #Round to two decimal points
            if distance > 2 and distance < 400:      #Check whether the distance is within range
                distance -= 0.5      #Print distance with 0.5 cm calibration
            else:
                distance = -1                   #display out of range
        else:
            distance = -1
        
        print distance, "cm"
        
if __name__ == '__main__':
    try:
        main()
    except:
        GPIO.cleanup()
        raise