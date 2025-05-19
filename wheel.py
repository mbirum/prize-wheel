from RPi import GPIO
from time import sleep
import time
import requests
import json
import sys
# import led

clk_pin = int(sys.argv[1])
dt_pin = int(sys.argv[2])
knob_increment = 1
spin_threshold = 25
github_token = ""

with open("/home/mattbirum/github/.token", "r") as file:
    github_token = file.read()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

min = 0
max = 1000000
position = 500
clk_last = GPIO.input(clk_pin)
dt_last = GPIO.input(dt_pin)
position_last = position

try:
	spin_started = False
	start_time = int(time.time())
	
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
	
		clk_last = clk
		dt_last = dt

		current_time = int(time.time())
		if (current_time > start_time): # check every full second
			if not spin_started:
				if (position - position_last) >= spin_threshold: 
					print(f'spin started - {position}')
					spin_started = True
			else:
				if position == position_last:
					print(f'stopped - {position}')
					spin_started = False
					# map position to inventory value
					value = 5
					url = 'https://api.github.com/repos/mbirum/prize-wheel/runs/15119304797/pending_deployments'
					headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {github_token}'}
					data = {'environment_ids': [6794031496], 'state': 'approved', 'comment': f'{value}'}
					try:
						response = requests.post(url, headers=headers, data=json.dumps(data))
						print(response)
					except Exception as e:
						print(e)
			position_last = position
			start_time = current_time
			
		sleep_interval = 0.0001
		sleep(sleep_interval)

finally:
	GPIO.cleanup()
	print('done')
