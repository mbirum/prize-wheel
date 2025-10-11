import time
import board
import busio
import adafruit_mpr121
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

increment = 0.06
input_buffer = []
buffer_size = 15
target_pin = 8

while True:
    mpr121[target_pin].value:
        print('Input {} touched!'.format(target_pin))
    else:
        print('|')
    sleep(increment)
