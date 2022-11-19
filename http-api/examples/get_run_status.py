import requests
import json


ROBOT_IP = "127.0.0.1"
RUN_ID = ""

HEADERS = {"opentrons-version": "3"}

runs_url = f"http://{ROBOT_IP}:31950/runs"
status_url = f"{runs_url}/{RUN_ID}"

r = requests.get(
	url=status_url,
	headers=HEADERS
	)

run_status = json.loads(r.text)
print(f"Run status:\n{run_status}")
