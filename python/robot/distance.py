import RPi.GPIO as GPIO                    #Import GPIO library
import sys, os
import time                                #Import time library
import sched
from hcsr04 import hcsr04
import threading

counter = 0

def main():
    GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

    in1_pin = 4
    in2_pin = 17
    en_pin = 27

    GPIO.setup(in1_pin, GPIO.OUT)
    GPIO.setup(in2_pin, GPIO.OUT)
    GPIO.setup(en_pin, GPIO.OUT)

    GPIO.output(en_pin, GPIO.HIGH)
    pwm = GPIO.PWM(in2_pin, 500)
    GPIO.output(in1_pin, GPIO.LOW)
    #GPIO.output(in2_pin, GPIO.HIGH)
    pwm.start(50)

    scheduler = sched.scheduler(time.time, time.sleep)
    sensor = hcsr04(12, 16)
    print "Threads alive: ", threading.active_count()
    print "Thread Enumerate: ", threading.enumerate()
    trigger(sensor)
    scheduler.enter(1, 1, trigger, (sensor,))
    
    for x in range (1, 20):
        scheduler.enter(x*5, 1, trigger, (sensor,))
    scheduler.run()
    GPIO.cleanup()

def trigger(sensor):
    sensor.trigger();
    time.sleep(3)
    print sensor.get_distance(), "cm"
    
if __name__ == '__main__':
    try:
        main()
    except:
        GPIO.cleanup()
        raise