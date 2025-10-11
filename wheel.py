import adafruit_mpr121
from time import sleep
import sys
import os

#channel = sys.argv[1]

increment = 0.01

i2c = board.I2C()
cap = adafruit_mpr121.MPR121_I2C(i2c)
#cap = MPR121.MPR121()
if not cap.begin():
    print('Error initializing MPR121')
    sys.exit(1)

last_touched = cap.touched()
while True:
    
    current_touched = cap.touched()
    
    for i in range(12):    
        pin_bit = 1 << i

        # If transitioning to touched from not touched
        if current_touched & pin_bit and not last_touched & pin_bit:
            print(f'Touched {i}!')
        
        if not current_touched & pin_bit and last_touched & pin_bit:
            print(f'{i} is no longer being touched')

    last_touched = current_touched
    sleep(increment)
