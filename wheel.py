import time
import board
import busio
import adafruit_mpr121
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

increment = 0.06

while True:
    for i in range(12):
        if i == 8 and mpr121[i].value:
            print('Input {} touched!'.format(i))
        elif i == 8:
            print('|')
    sleep(increment)
