import pigpio                     # Use GPIO

Pin18 = 18                        # Output on BCM pin 18
Frequency = 100000                # Set output frequency to 100KHz
DutyCycle = 500000                # Set duty cycle to 50%

pi = pigpio.pi()                  # initialize GPIO
pi.hardware_PWM(Pin18,Frequency,DutyCycle) # set up hardware PWM on pin
