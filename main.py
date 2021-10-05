import pigpio                                       # Use GPIO
import smbus                                        # use for I2C
import time                                         # use for timing

# Declare Variables
Pin18 = 18                                          # Output on BCM pin 18
Frequency = 100000                                  # Set output frequency to 100KHz
ActualDutyCycle = 50
delay = 0.2
PotAddr = 0x52                                      # I2C address of potentiometer
Channel = 1                                         # I2C channel 1

# Initialize Stuffs
pi = pigpio.pi()                                    # initialize GPIO
bus = smbus.SMBus(Channel)                          # initialize I2C (SMBus)
bus.write_byte_data(PotAddr,2,0x00)                 # write configuration register 2 for auto-conversion

def read_ADC():
    temp = bus.read_word_data(PotAddr,0)                # read word
    AD = (((temp&0xFF00)>>8) | ((temp&0x00FF)<<8))>>2   # re-arrange word
    Voltage = AD/1023.0*3.30                            # convert to voltage (ref 3.3V)
    print("Voltage: " + str(Voltage))
    return Voltage

def convert_Actual_Duty_Cycle(ActualDutyCycle):
    return ActualDutyCycle*10000

def vary_Duty_Cycle(initial_duty, final_duty, step, delay):
    for i in range(initial_duty, final_duty+step, step):
        print("Duty Cycle: " + str(i) + "%")
        pi.hardware_PWM(Pin18,Frequency,convert_Actual_Duty_Cycle(i))
        time.sleep(delay)

while(1):
    print("\n\n======================")
    print("Delay: " + str(delay) + " seconds")
    ref_voltage = read_ADC()
    vary_Duty_Cycle(0, 100, 5, delay)
    time.sleep(0.1)