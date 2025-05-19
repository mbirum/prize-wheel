from RPi import GPIO
from time import sleep
import sys
import os
# import led

clk_pin = int(sys.argv[1])
dt_pin = int(sys.argv[2])
knob_increment = int(sys.argv[3])
knob_increment = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

min = 0
max = 127
position = min
clk_last = GPIO.input(clk_pin)
dt_last = GPIO.input(dt_pin)
position_last = position

try:
	spin_started = False
	
	while True:
		clk = GPIO.input(clk_pin)
		dt = GPIO.input(dt_pin)
		full = True
	
		#half or full click
		if clk != dt:
			full = False
	      
		if full:
			#left click
			if clk_last != clk and dt_last == dt:
				position -= knobIncrement
				if position < min:
					position = max # loop back
			#right click
			elif dt_last != dt and clk_last == clk:
				position += knobIncrement
				if position > max:
					position = min # loop back
	
		if position_last != position:
			if not spin_started:
				spin_started = True
		else:
			if spin_started:
				spin_started = False
				print(f'Stopped! - {position}')
	
		clk_last = clk
		dt_last = dt
	
		position_last = position
		
		sleep_interval = 0.01
		sleep(sleep_interval)

finally:
	GPIO.cleanup()
	print('done')
