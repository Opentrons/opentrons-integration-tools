import requests
import json


ROBOT_IP = "127.0.0.1"
PROTOCOL_ID = ""

HEADERS = {"opentrons-version": "3"}

runs_url = f"http://{ROBOT_IP}:31950/runs"
protocol_id_payload = json.dumps({"data":{"protocolId": PROTOCOL_ID}})

r = requests.post(
	url=runs_url,
	headers=HEADERS,
	data=protocol_id_payload
	)

r_dict = json.loads(r.text)
run_id = r_dict["data"]["id"]

print(f"Run ID:\n{run_id}")
