# Opentrons HTTP API

Starting in software version 5.0, the Opentrons App manages and runs protocols using HTTP API exposed by the robot. This API is not (yet) formally documented, but it is functional and usable. This directory contains examples of some common tasks that the API can be used for. The complete command set can be found in the OpenAPI documentation.

## Overview

The Opentrons HTTP API is a REST-ful API that communicates via JSON request and response bodies. Since it is the primary method of communication between the Opentrons App and the robot, anything you can do with the App you can do with the HTTP API directly! (That being said, some things are easier to accomplish than others.)

The HTTP API is versioned independently of the overall software with a simple integer version to ensure stability through software updates. To request a specific version of the HTTP API, use the `Opentrons-Version` header. At the time of writing, the latest HTTP API version is `3`. For testing purposes, you may also request `Opentrons-Version: *`, which mean means "give me the latest version you have," but you should not use this in actual workflows.

## OpenAPI Documentation

The API uses the OpenAPI specification and has documentation that is auto-generated with Redoc. The specification can be found at:

<http://${ROBOT_IP}:31950/openapi.json>

and the generated documentation can be found at:

<http://${ROBOT_IP}:31950/redoc>

It may be convenient to generate a static HTML file of the documentation with [redoc-cli](https://redocly.com/docs/redoc/deployment/cli/).

## Examples

The examples below use `curl`, and assume you are running a Linux, macOS, or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) shell. Before trying these examples, get the IP address of your robot and enter the following in your terminal:

```shell
# replace with actual IP address
export ROBOT_IP=192.168.1.1
```

This IP address will then be used if you copy and paste the snippets below into the same terminal window.

### 1: Simple Commands

There are a few "simple" commands that can be run in isolation, independent of the state of the robot. Sending a "simple command" to the robot involves sending a `POST` request with details about the command to the `/commands` endpoint. The availble commands (and other related endpoints) are documented under <http://${ROBOT_IP}:31950/redoc#tag/Simple-Commands>.

#### Home the robot

```shell
curl -X POST "http://${ROBOT_IP}:31950/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "home", "params": {} } }'
```

#### Home the pipettes

```shell
# home the left pipette Z-stage and plunger
curl -X POST "http://${ROBOT_IP}:31950/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "home", "params": { "axes": ["leftZ", "leftPlunger"] } } }'

# home the right pipette Z-stage and plunger
curl -X POST "http://${ROBOT_IP}:31950/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "home", "params": { "axes": ["rightZ", "rightPlunger"] } } }'
```

#### Turn rail lights on and off

```shell
# turn the rail lights on
curl -X POST "http://${ROBOT_IP}:31950/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "setRailLights", "params": { "on": true } } }'

# turn the rail lights off
curl -X POST "http://${ROBOT_IP}:31950/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "setRailLights", "params": { "on": false } } }'
```

### 2: Running a Protocol File

You may use the HTTP API to:

1. Upload a protocol file and optional custom labware
2. Create a run of that protocol file
3. Start, pause, or stop that run

#### Step 1. Upload a protocol

The first step to running a protocol is to give the robot your protocol file. This is done through a call to `POST /protocols`.

```shell
# upload `example_protocol.py`
curl -X POST "http://${ROBOT_IP}:31950/protocols" \
    -H "Opentrons-Version: 3" \
    -F "files=@example_protocol.py"

# upload `example_protocol.py` and custom labware `example_labware.json`
curl -X POST "http://${ROBOT_IP}:31950/protocols" \
    -H "Opentrons-Version: 3" \
    -F "files=@example_protocol.py" \
    -F "files=@example_labware.json"
```

You will receive a response that looks something like this:

```json
{
  "data": {
    "id": "d97883b2-ec45-4dc3-82e3-62b7be8155ab",
    "createdAt": "2022-11-23T19:27:34.349238+00:00",
    "files": [
      { "name": "example_protocol.py", "role": "main" },
      { "name": "example_labware.json", "role": "labware" }
    ],
    "protocolType": "python",
    "metadata": { "apiLevel": "2.13" },
    "analysisSummaries": [
      { "id": "6dfb2a6e-7e06-4272-892a-205878c98b3e", "status": "pending" }
    ]
  }
}
```

This has a few important outputs:

- `data.id` - The unique identifier on the robot of this protocol upload. **Use this ID to create runs of this protocol.**
- `data.analysisSummaries[].id` - An idetifier of a protocol analysis that was kicked off by the upload. You can use this ID to retrieve the robot's idea of what the protocol will do when you run it

To retrieve the protocol analysis, use both these IDs in a new `GET` request:

```shell
curl -X GET "http://${ROBOT_IP}:31950/protocols/${protocol_id}/analyses/${analysis_id}" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json"
```

See the following example Python files for more details:

- [upload_protocol.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/upload_protocol.py)
- [upload_protocol_custom_labware.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/upload_protocol_custom_labware.py)

#### Step 2: Create a protocol “run”

Once you have given the robot your protocol file, you can create a "run" of that file using `POST /runs`. The same protocol upload can be used to create multiple runs; you do not need to re-upload the protocol file if it has not changed.

```shell
# create a run using the protocol ID from the previous step
curl -X POST "http://${ROBOT_IP}:31950/runs" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "protocolId": "${protocol_id}" } }'
```

You will get a response back that looks something like:

```json
{
  "data": {
    "id": "c5c3bca8-7b98-4008-929f-ee86627edc3f",
    "createdAt": "2022-11-23T19:36:30.183623+00:00",
    "status": "idle",
    "current": true,
    "actions": [],
    "errors": [],
    "pipettes": [],
    "modules": [],
    "labware": [
      {
        "id": "fixedTrash",
        "loadName": "opentrons_1_trash_1100ml_fixed",
        "definitionUri": "opentrons/opentrons_1_trash_1100ml_fixed/1",
        "location": { "slotName": "12" }
      }
    ],
    "labwareOffsets": [],
    "protocolId": "d97883b2-ec45-4dc3-82e3-62b7be8155ab"
  }
}
```

This response has a few important outputs

- `data.id` - The unique identifier of this run. **Use this ID in subsequent requests to get the status of the run and control it.**
- `data.protocolId` - The idetifier of the protocol that's being run
- `data.status`- The status of the run, which will start as `idle`

See the following example Python files for more details:

- [create_run_from_protocol.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/create_run_from_protocol.py)

#### Step 3: Play (start/resume), pause, stop (cancel) protocol run

You can control the run using the `POST /runs/${run_id}/actions` endpoint using the run ID from the create request.

```shell
# start or resume the run
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/actions" \
    -H "Opentrons-Version: 3"
    -H "Content-Type: application/json"
    -d '{ "data": { "actionType": "play" } }'

# pause the run
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/actions" \
    -H "Opentrons-Version: 3"
    -H "Content-Type: application/json"
    -d '{ "data": { "actionType": "pause" } }'

# cancel the run
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/actions" \
    -H "Opentrons-Version: 3"
    -H "Content-Type: application/json"
    -d '{ "data": { "actionType": "stop" } }'
```

See the following example Python files for more details:

- [play_run.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/play_run.py)
- [pause_run.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/pause_run.py)
- [stop_run.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/stop_run.py)

#### Step 4: Get run status

Before, during, and after the run, you can use the `GET /runs/${run_id}` and `GET /runs/${run_id}/commands` endpoints to track the status of the run using its ID. Note that the `.../commands` endpoint is paginated, and will return the last `20` commands by default. Use the `pageLength` query parameter to change the number of commands returned.

```shell
# get the status of the run
curl -X GET "http://${ROBOT_IP}:31950/runs/${run_id}" \
    -H "Opentrons-Version: 3"
    -H "Content-Type: application/json"

# get the status of the commands
curl -X GET "http://${ROBOT_IP}:31950/runs/${run_id}/commands" \
    -H "Opentrons-Version: 3"
    -H "Content-Type: application/json"
```

See the following example Python files for more details:

- [get_run_status.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/get_run_status.py)

#### Other helpful requests

Get a list of the last 20 uploaded protocols:

```shell
curl "http://${ROBOT_IP}:31950/protocols" -H "Opentrons-Version: 3"`
```

[get_protocols_list.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/get_protocols_list.py)

Get a list of the last 20 runs:

```shell
curl "http://${ROBOT_IP}:31950/runs" -H "Opentrons-Version: 3"`
```

[get_runs_list.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/get_runs_list.py)

#### Optional cleanup

By default, the robot will only keep the last 20 protocols and the last 20 runs in its database. You may also remove them from the database manually.

```shell
# delete a run by ID
curl -X DELETE "http://${ROBOT_IP}:31950/runs/${run_id}" -H "opentrons-version: 3"`

# delete a protocol by ID
curl -X DELETE "http://${ROBOT_IP}:31950/protocols/${protocol_id}" -H "opentrons-version: 3"`
```

The robot will not allow you to delete any protocols that are still referred to by any runs.

See the following Python examples for more details:

- [delete_run.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/delete_run.py)
- [delete_protocol.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/delete_protocol.py)

### 3: Atomic Liquid Handling Actions

Revisiting the "Main Flow" in Section 2: you may use the HTTP API to issue individual liquid handling commands directly to the robot, **without the use of a protocol file**. To get started, create a "run" _without_ an associated protocol ID:

```shell
curl -X POST "http://${ROBOT_IP}:31950/runs" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": {} }'
```

From here, you can issue commands using `POST /runs/${run_id}/commands`. For example, you can load a tip rack:

```shell
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "loadLabware", "params": { "loadName": "opentrons_96_tiprack_300ul", "namespace": "opentrons", "version": 1, "location": { "slotName": "6" } } } }'
```

You'll get back a response that looks something like:

```json
{
    "data": {
        "id": "949ec07c-230f-499f-8ef9-a4a04a5a51aa",
        "createdAt": "2022-11-23T20:10:50.038834+00:00",
        "commandType": "loadLabware",
        "key": "949ec07c-230f-499f-8ef9-a4a04a5a51aa",
        "status": "succeeded",
        "params": {
            "location": { "slotName": "6" },
            "loadName": "opentrons_96_tiprack_300ul",
            "namespace": "opentrons",
            "version": 1
        },
        "result": {
            "labwareId": "03fe9b55-64ce-4c86-9394-78049ebb93c4",
            "definition": { ... },
        },
        "startedAt": "2022-11-23T20:10:50.039308+00:00",
        "completedAt": "2022-11-23T20:10:50.048137+00:00",
        "intent": "setup"
    }
}
```

From here, you can use `data.result.labwareId` to refer to this labware in future requests.

You can also load a pipette:

```shell
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "loadPipette", "params": { "pipetteName": "p300_single_gen2", "mount": "right" } } }'
```

You'll get back a response that looks something like:

```json
{
  "data": {
    "id": "9c10dc84-741b-491a-a409-254726da7bc4",
    "createdAt": "2022-11-23T20:15:02.831678+00:00",
    "commandType": "loadPipette",
    "key": "9c10dc84-741b-491a-a409-254726da7bc4",
    "status": "succeeded",
    "params": {
      "pipetteName": "p300_single_gen2",
      "mount": "right"
    },
    "result": {
      "pipetteId": "5798c352-c672-4241-81fd-a6f4da43b07f"
    },
    "startedAt": "2022-11-23T20:15:02.831782+00:00",
    "completedAt": "2022-11-23T20:15:02.835556+00:00",
    "intent": "setup"
  }
}
```

From here, you can use `data.result.pipetteId` to refer to this labware in future requests.

With a pipette and a tip rack loaded, you can instruct the pipette to pick up tip `A1` from the labware:

```shell
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/commands?waitUntilComplete=true" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "pickUpTip", "params": { "pipetteId": "${pipette_id}", "labwareId": "${labware_id}", "wellName": "A1" } } }'
```

By default, commands sent via `POST /runs/${run_id}/commands` are classified as `setup` commands (see: `"intent": "setup"` in the responses), which means they will run immediately once they're created. This is especially useful for commands like `loadLabware` and `loadPipette`, but can be used to run any available command(s) "live."

You can also choose to queue up several commands that will not run until you issue a `POST .../actions { "actionType": "play" }` as you would when running a protocol file. To queue protocol commands, omit the `waitUntilComplete` query parameter from the URL and use `"intent": "protocol"` in your request body:

```shell
curl -X POST "http://${ROBOT_IP}:31950/runs/${run_id}/commands" \
    -H "Opentrons-Version: 3" \
    -H "Content-Type: application/json" \
    -d '{ "data": { "commandType": "dropTip", "intent": "protocol", "params": { "pipetteId": "${pipette_id}", "labwareId": "${labware_id}", "wellName": "A1" } } }'
```

See the following Python examples for more details:

- [atomic_commands_setup.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/atomic_commands_setup.py)
- [atomic_liquid_handling.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/atomic_liquid_handling.py)
- [atomic_move_to_well.py](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/atomic_move_to_well.py)
- [atomic_moves_advanced.pu](https://github.com/Opentrons/opentrons-integration-tools/blob/main/http-api/examples/atomic_moves_advanced.py)
