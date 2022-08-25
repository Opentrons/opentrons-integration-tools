# Door Sensor

The status of the door can be gotten in multiple layers of the Opentrons software stack:

### Opentrons App

https://support.opentrons.com/s/article/Pause-a-protocol-when-the-robot-door-opens

### Protocol API

https://docs.opentrons.com/v2/new_protocol_api.html#opentrons.protocol_api.contexts.ProtocolContext.door_closed

### Hardware Control API

https://github.com/Opentrons/opentrons/blob/edge/api/src/opentrons/hardware_control/api.py

`door_state` property

### GPIO Driver

https://github.com/Opentrons/opentrons/blob/edge/api/src/opentrons/drivers/rpi_drivers/gpio.py

`get_door_state()` function
