import pigpio                                       # Use GPIO
import smbus                                        # use for I2C
import time                                         # use for timing

# Declare Variables
Pin18 = 18                                          # Output on BCM pin 18
Frequency = 100000                                  # Set output frequency to 100KHz   
# PotAddr = 0x52                                    # I2C address of Potentiometer
PotAddr = 0x51                                      # I2C address of Output
Channel = 1                                         # I2C channel 1

# Initialize Stuffs
pi = pigpio.pi()                                    # initialize GPIO
bus = smbus.SMBus(Channel)                          # initialize I2C (SMBus)
bus.write_byte_data(PotAddr,2,0x00)                 # write configuration register 2 for auto-conversion

def read_ADC_Output_Voltage():
    temp = bus.read_word_data(PotAddr,0)                # read word
    AD = (((temp&0xFF00)>>8) | ((temp&0x00FF)<<8))>>2   # re-arrange word
    Output_Voltage = AD/1023.0*3.30 * 4                 # convert to voltage (ref 3.3V), multiply by 4 
    return Output_Voltage

def convert_Actual_Duty_Cycle(ActualDutyCycle):
    return ActualDutyCycle*10000

def vary_Duty_Cycle(initial_duty, final_duty, step, delay):
    for i in range(initial_duty, final_duty+step, step):
        print("Duty Cycle: " + str(i) + "%")
        pi.hardware_PWM(Pin18,Frequency,convert_Actual_Duty_Cycle(i))       # Write to pin
        time.sleep(delay)

def continuously_vary_duty_cycle(step, delay):
    vary_Duty_Cycle(0, 100, step, delay)            # Increase the duty cycle from 0 to 100 by steps, with a delay in between
    vary_Duty_Cycle(100-step, step, step, delay)    # Decrease the duty cycle from 100-step to step, with a delay in between

def toggle_between_duty_cycle(duty_1, duty_2):
    pi.hardware_PWM(Pin18,Frequency,convert_Actual_Duty_Cycle(duty_1))      # Set duty cycle to 40
    time.sleep(10)                                                          # Wait for 10s
    pi.hardware_PWM(Pin18,Frequency,convert_Actual_Duty_Cycle(duty_2))      # Set duty cycle to 40
    time.sleep(10)                                                          # Wait for 10s

def clear_text_file(file_name):
    file = open(file_name,"r+")
    file.truncate(0)
    file.close()

def P_control():
    clear_text_file("output.txt")                               # Clear the text file and closes it
    text_file = open("output.txt", "a")                         # Open text file in append mode

    # Parameters for control
    k = 0.093                                                   # system gain
    kp = 0.1                                                    # Kp
    w = 6                                                       # reference_voltage
    u0 = w/k                                                    # Duty cycle is calculated from reference voltage divide by system gain
    count = 0                                                   # Loop Counter

    while(1):
        y = read_ADC_Output_Voltage()                           # output_voltage
        e =  w - y                                              # Calculate Error
        u = kp * e + u0                                         # Calculate Duty Cycle
        
        if u > 100:                                             # We need to limit our U. A duty cycle that is negative or over 100 does not make sense!
            u = 100
        elif u < 0:
            u = 0

        pi.hardware_PWM(Pin18, Frequency, (100-u)*10000)        # Write the calculated U (PWM) to pin
        
        count += 1                                              # Increment Loop Counter
        if count == 100:
            count = 0                                           # Reset counter
            kp *= 3                                             # Increment Kp
            if kp > 25:                                         # If Kp is more than 25, end control
                break
        
        output_string = "y: " + str(round(y,3)) + ", w: " + str(round(w,3)) + ", Error: " + str(round(e,3)) + ", kp: " + str(kp) + ", duty cycle: " + str(round(u,3)) + "\n"
        print(output_string)
        text_file.write(output_string)                          # Append the print line to text file for plotting

    text_file.close()

while(1):
    # P Control
    P_control()

    # Vary duty cycle (Staircase Test)
    # delay = 0.2
    # step = 20
    # continuously_vary_duty_cycle(step, delay)

    # Toggle duty cycle between duty_cycle 1 and duty_cycle 2
    # duty_1 = 40
    # duty_2 = 60
    # toggle_between_duty_cycle(duty_1, duty_2)
    
    
    

