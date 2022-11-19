# Opentrons HTTP API
Starting in software version 5.0, the Opentrons app manages and runs protocols using HTTP. The API for this is not (yet) formally documented or meant to be used by other clients besides the Opentrons app, but it is functional and usable. This directory contains examples of some common tasks that the API can be used for. The complete command set can be found in the OpenAPI documentation.

### OpenAPI Documentation
The API uses the OpenAPI specification and has documentation that is auto-generated with Redoc. The specification can be found at:

`http://ROBOT_IP:31950/openapi.json`

and the Redoc can be found at:

`http://ROBOT_IP:31950/redoc`

It may be convenient to generate a static HTML file of the documentation with [redoc-cli](https://redocly.com/docs/redoc/deployment/cli/).

### 1: Simple Commands
There are a few "simple" commands that can be run in isolation, independent of the state of the robot.

Home the robot:

`curl -X POST "http://ROBOT_IP:31950/robot/home" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"target":"robot"}'`

Home the pipettes:

`curl -X POST "http://ROBOT_IP:31950/robot/home" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"target":"pipette", "mount": "left"}'`

`curl -X POST "http://ROBOT_IP:31950/robot/home" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"target":"pipette", "mount": "right"}'`

Rail lights (get status, and turn on/off):

`curl "http://ROBOT_IP:31950/robot/lights" -H "opentrons-version: 3"`

`curl -X POST "http://ROBOT_IP:31950/robot/lights" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"on":true}'`

`curl -X POST "http://ROBOT_IP:31950/robot/lights" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"on":false}'`

Warning: the `/robot/move` endpoint is deprecated and probably does not behave how you want it to.

### 2: Running a Protocol
#### Main Flow
Step 1: Upload a protocol

Input: protocol file, custom labware file (optional)

Returns: protocol ID

`curl -X POST "http://ROBOT_IP:31950/protocols" -H "Opentrons-Version: 3" -F "files=@example_protocol.py"`

`curl -X POST "http://ROBOT_IP:31950/protocols" -H "Opentrons-Version: 3" -F "files=@example_protocol.py" -F "files=@example_labware.json"`

Step 2: Create a protocol “run”

Input: protocol ID

Returns: run ID

`curl -X POST "http://ROBOT_IP:31950/runs" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"data":{"protocolId":"PROTOCOL_ID"}}'`

Step 3: Play (start/resume), pause, stop (cancel) protocol run 

Input: run ID

`curl -X POST "http://ROBOT_IP:31950/runs/RUN_ID/actions" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"data":{"actionType":"play"}}'`

`curl -X POST "http://ROBOT_IP:31950/runs/RUN_ID/actions" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"data":{"actionType":"pause"}}'`

`curl -X POST "http://ROBOT_IP:31950/runs/RUN_ID/actions" -H "opentrons-version: 3" -H "Content-Type: application/json" -d '{"data":{"actionType":"stop"}}'`

Step 4: Get run status

Input: run ID

`curl "http://ROBOT_IP:31950/runs/RUN_ID" -H "opentrons-version: 3"`

#### Optional Information
Get list of protocols:

`curl "http://ROBOT_IP:31950/protocols" -H "opentrons-version: 3"`

Get list of runs:

`curl "http://ROBOT_IP:31950/runs" -H "opentrons-version: 3"`

#### Optional cleanup

Delete a run:

Input: run ID

`curl -X DELETE "http://ROBOT_IP:31950/runs/RUN_ID" -H "opentrons-version: 3"`

Delete a protocol:

Input: protocol ID

`curl -X DELETE "http://ROBOT_IP:31950/protocols/PROTOCOL_ID" -H "opentrons-version: 3"`

### 3: Atomic Liquid Handling Actions
Revisiting the "Main Flow" in Section 2: the API allows for the creation of a protocol "run" that is not associated with a "protocol". Using the `runs/RUN_ID/commands` endpoint, you first send "Setup" commands (`"intent": "setup"`) to specify the robot and deck setup (pipettes, labware, modules). You can then enqueue "Protocol" commands (`"intent": "protocol"`) and send a "play" signal to dynamically add steps and run the protocol.

To add even more flexibility: running every command with `"intent: setup"` allows for true atomic actions on demand, without being tied to protocol steps.
