# Send atomic liquid handling commands to a run that has been set up

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
Liquid handling commands
"""
# Pick up tip
command_dict = {
	"data": {
		"commandType": "pickUpTip",
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


# Aspirate
command_dict = {
	"data": {
		"commandType": "aspirate",
		"params": {
			"labwareId": labware_2_id,
			"wellName": "A1",
			"wellLocation": {
				"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
			},
			"flowRate": 0.75,
			"volume": 50,
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


# Dispense
command_dict = {
	"data": {
		"commandType": "dispense",
		"params": {
			"labwareId": labware_2_id,
			"wellName": "A2",
			"wellLocation": {
				"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
			},
			"flowRate": 0.75,
			"volume": 50,
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


# Blowout
command_dict = {
	"data": {
		"commandType": "blowout",
		"params": {
			"labwareId": labware_2_id,
			"wellName": "A2",
			"wellLocation": {
				"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
			},
			"flowRate": 1.23,
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


# Drop tip
command_dict = {
	"data": {
		"commandType": "dropTip",
		"params": {
			"labwareId": "fixedTrash",
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
