import requests
import json


ROBOT_IP = "127.0.0.1"

HEADERS = {"opentrons-version": "3"}

protocols_url = f"http://{ROBOT_IP}:31950/protocols"

r = requests.get(
	url=protocols_url,
	headers=HEADERS
	)

protocols_dict = json.loads(r.text)
print("Protocols list:")
for p in protocols_dict["data"]:
	print(p)
