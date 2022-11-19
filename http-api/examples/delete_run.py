import requests
import json


ROBOT_IP = "127.0.0.1"
RUN_ID = ""

HEADERS = {"opentrons-version": "3"}

runs_url = f"http://{ROBOT_IP}:31950/runs"
delete_run_url = f"{runs_url}/{RUN_ID}"

r = requests.delete(
	url=delete_run_url,
	headers=HEADERS
	)

print(f"Request status:\n{r}\n{r.text}")