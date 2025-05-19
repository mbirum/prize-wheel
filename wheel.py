from RPi import GPIO
from time import sleep
import time
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
max = 1000000
position = min
clk_last = GPIO.input(clk_pin)
dt_last = GPIO.input(dt_pin)
position_last = position

try:
	potential_spin = False
	potential_spin_position = position
	spin_started = False
	potential_stop = False
	movement_start_time = None
	movement_stop_time = None
	spin_start_time = None
	
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
				position -= knob_increment
				if position < min:
					position = max # loop back
			#right click
			elif dt_last != dt and clk_last == clk:
				position += knob_increment
				if position > max:
					position = min # loop back
	
		if position_last != position:
			if not spin_started:
				if not potential_spin:
					print('potential spin')
					potential_spin = True
					movement_start_time = int(time.time())
					potential_spin_position = position
				else:
					current_time = int(time.time())
					time_diff = int(current_time - movement_start_time)
					position_diff = position - potential_spin_position
					if time_diff >= 1:
						if position_diff >= 10:
							print('spin started')
							spin_started = True
						else:
							print('spin reset')
						potential_spin = False
		else:
			if not potential_stop:
				if spin_started:
					print('potential stop')
					potential_stop = True
					movement_stop_time = int(time.time())
			else:
				current_time = int(time.time())
				time_diff = int(current_time - movement_stop_time)
				if time_diff >= 1:
					spin_started = False
					potential_stop = False
					print(f'Stopped! - {position}')
	
		clk_last = clk
		dt_last = dt
	
		position_last = position
		
		sleep_interval = 0.001
		sleep(sleep_interval)

finally:
	GPIO.cleanup()
	print('done')
