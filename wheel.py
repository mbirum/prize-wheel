from RPi import GPIO
from time import sleep
import time
import sys
import os
# import led

clkPin = int(sys.argv[1])
dtPin = int(sys.argv[2])
knobIncrement = int(sys.argv[3])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(clkPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dtPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

min = 0
max = 127
pos = min
clkLast = GPIO.input(clkPin)
dtLast = GPIO.input(dtPin)
posLast = pos

try:
	checks = []
	spin_started = False
	spin_start_time = None
	
	while True:
		clk = GPIO.input(clkPin)
		dt = GPIO.input(dtPin)
		full = True
	
		#half or full click
		if clk != dt:
			full = False
	      
		if full:
			#left click
			if clkLast != clk and dtLast == dt:
				pos -= knobIncrement
				if pos < min:
					pos = max # loop back
			#right click
			elif dtLast != dt and clkLast == clk:
				pos += knobIncrement
				if pos > max:
					pos = min # loop back
	
		if posLast != pos:
			if not spin_started:
				spin_started = True
		else:
			if spin_started:
				spin_started = False
				print(f'Stopped! - {pos})
	
		clkLast = clk
		dtLast = dt
	
		posLast = pos
		
		sleep_interval = 0.01
		sleep(sleep_interval)

finally:
	GPIO.cleanup()
	print('done')
