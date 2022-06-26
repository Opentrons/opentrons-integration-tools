# Move the gantry in the XY plane with an Xbox 360 controller
# Uses the Opentrons Hardware Control API:
# https://github.com/Opentrons/opentrons/blob/edge/api/src/opentrons/hardware_control/api.py
# Run in Opentrons terminal; cannot be run as a Jupyter notebook

import asyncio

from opentrons import hardware_control
from opentrons import types

import xbox360_controller


async def main():

    # Default speed is 400 mm/s
    MOVE_SPEED = 150

    # How far to move in mm
    MOVE_DISTANCE = 20

    # Right or left mount
    MY_MOUNT = types.Mount.RIGHT

    # Xbox 360 controller instance
    my_xboxc = xbox360_controller.Xbox360ControllerDriver()

    # Opentrons hardware controller instance
    my_hc = await hardware_control.API.build_hardware_controller()

    print("Attached instruments:")
    print(my_hc.get_attached_instruments())

    print("Homing gantry")
    await my_hc.home()
    pos = await my_hc.current_position(MY_MOUNT)
    print("Current position:\n{}".format(pos))

    while True:
        print("Reading input")
        b = my_xboxc.read_input()
        print(b)

        # Left bumper or timeout: exit
        if b == 1 or b == -1:
            break

        # Right bumper: home gantry
        elif b == 2:
            await my_hc.home()
            pos = await my_hc.current_position(MY_MOUNT)
            print("Current position:\n{}".format(pos))

        # X button: move -X direction
        elif b == 64:
            await my_hc.move_rel(
                mount=MY_MOUNT,
                delta=(types.Point(x=-MOVE_DISTANCE, y=0, z=0)),
                speed=MOVE_SPEED
                )
            pos = await my_hc.current_position(MY_MOUNT)
            print("Current position:\n{}".format(pos))

        # B button: move +X direction
        elif b == 32:
            await my_hc.move_rel(
                mount=MY_MOUNT,
                delta=(types.Point(x=MOVE_DISTANCE, y=0, z=0)),
                speed=MOVE_SPEED
                )
            pos = await my_hc.current_position(MY_MOUNT)
            print("Current position:\n{}".format(pos))

        # A button: move -Y direction
        elif b == 16:
            await my_hc.move_rel(
                mount=MY_MOUNT,
                delta=(types.Point(x=0, y=-MOVE_DISTANCE, z=0)),
                speed=MOVE_SPEED
                )
            pos = await my_hc.current_position(MY_MOUNT)
            print("Current position:\n{}".format(pos))

        # Y button: move +Y direction
        elif b == 128:
            await my_hc.move_rel(
                mount=MY_MOUNT,
                delta=(types.Point(x=0, y=MOVE_DISTANCE, z=0)),
                speed=MOVE_SPEED
                )
            pos = await my_hc.current_position(MY_MOUNT)
            print("Current position:\n{}".format(pos))

        my_xboxc.cleanup()


asyncio.run(main())
