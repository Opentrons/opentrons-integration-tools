import requests
import json


ROBOT_IP = "127.0.0.1"
PROTOCOL_FILE = "example_protocol.py"
LABWARE_FILE = "example_labware.json"

HEADERS = {"opentrons-version": "3"}

protocols_url = f"http://{ROBOT_IP}:31950/protocols"
protocol_file_payload = open(PROTOCOL_FILE, "rb")
labware_file_payload = open(LABWARE_FILE, "rb")

r = requests.post(
	url=protocols_url,
	headers=HEADERS,
	files=[("files", protocol_file_payload), ("files", labware_file_payload)]
	)

r_dict = json.loads(r.text)
protocol_id = r_dict["data"]["id"]
print(f"Protocol ID:\n{protocol_id}")

protocol_file_payload.close()
labware_file_payload.close()
