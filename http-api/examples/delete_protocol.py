import requests
import json


ROBOT_IP = "127.0.0.1"
PROTOCOL_ID = ""

HEADERS = {"opentrons-version": "3"}

protocols_url = f"http://{ROBOT_IP}:31950/protocols"
delete_protocol_url = f"{protocols_url}/{PROTOCOL_ID}"

r = requests.delete(
	url=delete_protocol_url,
	headers=HEADERS
	)

print(f"Request status:\n{r}\n{r.text}")
