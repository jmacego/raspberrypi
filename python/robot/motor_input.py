import time
import sys, os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
in1_pin = 4
in2_pin = 17
en_pin = 27

def setup():
    GPIO.setup(in1_pin, GPIO.OUT)
    GPIO.setup(in2_pin, GPIO.OUT)
    GPIO.setup(en_pin, GPIO.OUT)
    GPIO.output(in1_pin, GPIO.HIGH)
    GPIO.output(in2_pin, GPIO.HIGH)
    GPIO.output(en_pin, GPIO.HIGH)
        
def main():
    setup()

    pwm1 = GPIO.PWM(in1_pin, 500)
    pwm2 = GPIO.PWM(in2_pin, 500)
    pwm1.start(50)
    pwm2.start(50)

    while True:
        input1 = input("Input 1: ")
        input2 = input("Input 2: ")
        pwm1.ChangeDutyCycle(input1)
        pwm2.ChangeDutyCycle(input2)
        
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except:
        GPIO.cleanup()
        raise