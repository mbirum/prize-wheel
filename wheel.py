from RPi import GPIO
from time import sleep
import time
import requests
import json
import sys
import subprocess
# import led

clk_pin = int(sys.argv[1])
dt_pin = int(sys.argv[2])
knob_increment = 1
spin_threshold = 25
github_token = ""

with open("/home/mattbirum/github/.token", "r") as file:
	for line in file:
		if line and len(line) > 0:
			github_token = line.strip()
			
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

min = 0
max = 1000000
position = 500

subprocess.run(['git', '-C', '/home/mattbirum/prize-wheel', 'pull'])
inventory_count = 0
with open("/home/mattbirum/prize-wheel/inventory.txt", "rb") as f:
	inventory_count = sum(1 for _ in f)
item_min = 1
item_max = inventory_count
item_position = int((item_max + item_min) / 2)

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
				item_position -= knob_increment
				if item_position < item_min:
					item_position = item_max
					
			#right click
			elif dt_last != dt and clk_last == clk:
				position += knob_increment
				if position > max:
					position = min # loop back
				item_position += knob_increment
				if item_position > item_max:
					item_position = item_min
	
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
					spin_started = False
					
					subprocess.run(['git', '-C', '/home/mattbirum/prize-wheel', 'pull'])
					inventory_count = 0
					with open("/home/mattbirum/prize-wheel/inventory.txt", "rb") as f:
    						inventory_count = sum(1 for _ in f)
					value = item_position
					item_max = inventory_count - 1
					print(f'stopped - {position} - {value}')
					run_id = ""
					headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {github_token}'}
					url = 'https://api.github.com/repos/mbirum/prize-wheel/actions/runs?status=waiting'
					try:
						response = requests.get(url, headers=headers).json()
						run_id = response['workflow_runs'][0]['id']
						if not run_id or run_id == None:
							print('could not get run id. try again')
					except Exception as e:
						print(e)
						item_max = inventory_count
					url = f'https://api.github.com/repos/mbirum/prize-wheel/actions/runs/{run_id}/pending_deployments'
					data = {'environment_ids': [6794031496], 'state': 'approved', 'comment': f'{value}'}
					try:
						response = requests.post(url, headers=headers, data=json.dumps(data)).json()
						# print(response)
					except Exception as e:
						print(e)
						item_max = inventory_count
						
			position_last = position
			start_time = current_time
			
		sleep_interval = 0.0001
		sleep(sleep_interval)

finally:
	GPIO.cleanup()
	print('done')
