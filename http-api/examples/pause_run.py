import requests
import json


ROBOT_IP = "127.0.0.1"
RUN_ID = ""

HEADERS = {"opentrons-version": "3"}

runs_url = f"http://{ROBOT_IP}:31950/runs"
actions_url = f"{runs_url}/{RUN_ID}/actions"
action_payload = json.dumps({"data":{"actionType": "pause"}})

r = requests.post(
	url=actions_url,
	headers=HEADERS,
	data=action_payload
	)

print(f"Request status:\n{r}\n{r.text}")
