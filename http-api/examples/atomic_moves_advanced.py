# Send more advanced atomic move commands to a run that has been set up
# (You probably shouldn't run this on a real robot with anything on the deck!)

import requests
import json


ROBOT_IP = "127.0.0.1"
HEADERS = {"opentrons-version": "3"}

"""
Manually (for demo purposes) set IDs from run setup
"""
run_id = ""
labware_1_id = ""
labware_2_id = ""
pipette_id = ""

"""
Set up HTTP endpoints
"""
runs_url = f"http://{ROBOT_IP}:31950/runs"
commands_url = f"{runs_url}/{run_id}/commands"


"""
Move commands
"""
# Move to well 1
command_dict = {
	"data": {
		"commandType": "moveToWell",
		"params": {
			"labwareId": labware_1_id,
			"wellName": "A1",
			"wellLocation": {
				"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
			},
			"pipetteId": pipette_id
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}\n")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	data=command_payload
	)

print(f"Response:\n{r}\n{r.text}\n")


# Move to coordinates
command_dict = {
	"data": {
		"commandType": "moveToCoordinates",
		"params": {
			"coordinates": {"x": 200, "y": 200, "z": 600},
			"minimumZHeight": 500,
			"forceDirect": True,
			"pipetteId": pipette_id
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}\n")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	data=command_payload
	)

print(f"Response:\n{r}\n{r.text}\n")


# Relative move
command_dict = {
	"data": {
		"commandType": "moveRelative",
		"params": {
			"axis": "z",
			"distance": -20,
			"pipetteId": pipette_id
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}\n")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	data=command_payload
	)

print(f"Response:\n{r}\n{r.text}\n")
