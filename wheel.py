import time
import board
import busio
import adafruit_mpr121
from time import sleep

# initialize sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# initialize input buffer
input_buffer = []
buffer_size = 5
for i in range(buffer_size):
    input_buffer.append(False)

interval = 0.06
target_pin = 8
attempt_started = False

# started if buffer is all 'True'
def has_attempt_started():
    result = True
    for i in range(buffer_size):
        result = result and input_buffer[i]
    return result

while True:
    value = mpr121[target_pin].value
    input_buffer.pop(0)
    input_buffer.append(value)

    if value:
        if has_attempt_started():
            attempt_started = True
            print('SPIN!')
    else:
        if attempt_started:
            attempt_started = False
            print('stopped...')

    sleep(interval)




