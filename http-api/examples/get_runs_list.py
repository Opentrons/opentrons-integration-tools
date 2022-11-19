import requests
import json


ROBOT_IP = "127.0.0.1"

HEADERS = {"opentrons-version": "3"}

runs_url = f"http://{ROBOT_IP}:31950/runs"

r = requests.get(
	url=runs_url,
	headers=HEADERS
	)

runs_dict = json.loads(r.text)
print("Runs list:")
for r in runs_dict["data"]:
	print(r)
