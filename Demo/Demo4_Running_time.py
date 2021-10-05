
import RPi.GPIO as GPIO      # use for GPIO
import time                  # use for timing

Pin18 = 18                   # select pin 18

GPIO.setmode(GPIO.BCM)       # set to BCM mode
GPIO.setwarnings(False)      # disable warning
GPIO.setup(Pin18,GPIO.OUT)   # config pin to be output

delay = 0.1                  # set delay

while 1:                         # infinite loop
    GPIO.output(Pin18,GPIO.LOW)  # set pin to low
    time.sleep(delay)            # delay
    GPIO.output(Pin18,GPIO.HIGH) # now set pin to high
    time.sleep(delay)            # delay again by same amount
