import smbus                 # use for I2C
import time                  # use for timing

PotAddr = 0x52               # I2C address of potentiometer
Channel = 1                  # I2C channel 1

bus = smbus.SMBus(Channel)   # initialize I2C (SMBus)
bus.write_byte_data(PotAddr,2,0x00) # write configuration register 2 for auto-conversion

while 1:
    temp = bus.read_word_data(PotAddr,0)        # read word
    AD = (((temp&0xFF00)>>8) | ((temp&0x00FF)<<8))>>2   # re-arrange word
    Voltage = AD/1023.0*3.30                            # convert to voltage (ref 3.3V)
    print(AD,round(Voltage,4))                                   # print out the word
    time.sleep(0.1)                                       # delay 100ms
    
