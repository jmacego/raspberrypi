import time
import sys, os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


def main():

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

    time.sleep(200)
    #pwm1 = GPIO.PWM(4,500)
    #pwm2 = GPIO.PWM(17,500)

    #pwm1.start(50)

    #time.sleep(1)
    #pwm1.ChangeDutyCycle(0)
    #pwm2.start(50)
    #
    #time.sleep(1)
    #
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)