# Gets the state of the trash bin probe switches
# Have to run as Python script; not as Jupyter notebook
# Run "systemctl stop opentrons-robot-server" before running

import asyncio
from opentrons import hardware_control


async def main():

    my_hc_api = await hardware_control.API.build_hardware_controller()

    switches = await my_hc_api._backend._smoothie_driver.switch_state()

    # 1 if any probe switch pressed (trash bin is in), 0 if not
    probe_state = switches["Probe"]
    print(probe_state)

asyncio.run(main())
