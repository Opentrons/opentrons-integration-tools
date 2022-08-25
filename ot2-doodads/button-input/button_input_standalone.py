# Gets the state of the front button
# Have to run as Python script; not as Jupyter notebook
# Run "systemctl stop opentrons-robot-server" before running

import asyncio
from opentrons import hardware_control


async def main():
    
    my_hc_api = await hardware_control.API.build_hardware_controller()

    # True if button pressed, False if not
    button_state = my_hc_api._backend.gpio_chardev.read_button()
    print(button_state)

asyncio.run(main())