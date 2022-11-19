import requests
import json


ON = json.dumps({"on": True})
OFF = json.dumps({"on": False})

# Toggle for lights on/off
lights_status = ON

ROBOT_IP = "127.0.0.1"

HEADERS = {"opentrons-version": "3"}

lights_url = f"http://{ROBOT_IP}:31950/robot/lights"

# Change light status
r = requests.post(
	url=lights_url,
	headers=HEADERS,
	data=lights_status)

print(f"Request status:\n{r}\n{r.text}")

# Get lights status
r = requests.get(
	url=lights_url,
	headers=HEADERS
	)

print(f"Request status:\n{r}\n{r.text}")
