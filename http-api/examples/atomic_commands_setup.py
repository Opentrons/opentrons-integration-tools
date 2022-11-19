# Set up a run that can receive atomic commands

import requests
import json


ROBOT_IP = "127.0.0.1"
HEADERS = {"opentrons-version": "3"}

TIP_RACK = "opentrons_96_tiprack_300ul"
RESERVOIR = "nest_12_reservoir_15ml"
PIPETTE = "p300_single_gen2"


"""
Step 1: Create a run
"""
runs_url = f"http://{ROBOT_IP}:31950/runs"
print(f"Command:\n{runs_url}")

r = requests.post(
	url=runs_url,
	headers=HEADERS
	)

r_dict = json.loads(r.text)
run_id = r_dict["data"]["id"]
print(f"Run ID:\n{run_id}")


"""
Step 2: Set up commands endpoint
"""
commands_url = f"{runs_url}/{run_id}/commands"


"""
Step 3: "Setup" commands
"""
# Load labware 1 (tip rack)
command_dict = {
	"data": {
		"commandType": "loadLabware",
		"params": {
			"location": {"slotName": "6"},
			"loadName": TIP_RACK,
			"namespace": "opentrons",
			"version": 1
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	params={"waitUntilComplete": True},
	data=command_payload
	)

r_dict = json.loads(r.text)
labware_1_id = r_dict["data"]["result"]["labwareId"]
print(f"Labware 1 (tip rack) ID:\n{labware_1_id}\n")


# Load labware 2 (reservoir)
command_dict = {
	"data": {
		"commandType": "loadLabware",
		"params": {
			"location": {"slotName": "5"},
			"loadName": RESERVOIR,
			"namespace": "opentrons",
			"version": 1
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	params={"waitUntilComplete": True},
	data=command_payload
	)

r_dict = json.loads(r.text)
labware_2_id = r_dict["data"]["result"]["labwareId"]
print(f"Labware 2 (reservoir) ID:\n{labware_2_id}\n")


# Load pipette
command_dict = {
	"data": {
		"commandType": "loadPipette",
		"params": {
			"pipetteName": PIPETTE,
			"mount": "right"
		},
		"intent": "setup"
	}
}

command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}")

r = requests.post(
	url=commands_url,
	headers=HEADERS,
	params={"waitUntilComplete": True},
	data=command_payload
	)

r_dict = json.loads(r.text)
pipette_id = r_dict["data"]["result"]["pipetteId"]
print(f"Pipette ID:\n{pipette_id}\n")


"""
Step 4: Home the robot
"""
home_url = f"http://{ROBOT_IP}:31950/robot/home"
command_dict = {"target": "robot"}
command_payload = json.dumps(command_dict)
print(f"Command:\n{command_payload}")

r = requests.post(
	url=home_url,
	headers=HEADERS,
	data=command_payload
	)

print(f"Response:\n{r}\n{r.text}\n")


"""
Print all IDs in one place
"""
print("IDs for commands:")
print(f"Run ID:\n{run_id}")
print(f"Labware 1 (tip rack) ID:\n{labware_1_id}\n")
print(f"Labware 2 (reservoir) ID:\n{labware_2_id}\n")
print(f"Pipette ID:\n{pipette_id}\n")