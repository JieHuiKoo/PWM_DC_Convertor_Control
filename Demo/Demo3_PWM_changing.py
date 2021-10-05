import pigpio                # Use GPIO
import time                  # Use time

Pin18 = 18                   # Output on BCM pin 18
Frequency = 100000           # Set output frequency to 100KHz
DutyCycle = 0                # Set duty cycle to 0%

pi = pigpio.pi()                  # initialize GPIO
pi.hardware_PWM(Pin18,Frequency,DutyCycle) # set up hardware PWM on pin

while 1:                     # Infinite while loop ...
    for x in range(0,105,5): # Vary duty cycle from 0% to 100% at increment of 5%
        print(x)             # print out the current duty cycle
        pi.hardware_PWM(Pin18,Frequency,x*10000) # change duty cycle
        time.sleep(5)        # Wait five second
