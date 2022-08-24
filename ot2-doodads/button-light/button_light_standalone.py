# Lights up the front button in three different colors
# Have to run as Python script; not as Jupyter notebook
# Run "systemctl stop opentrons-robot-server" before running

import asyncio
from opentrons.drivers.rpi_drivers import build_gpio_chardev


async def main():

    my_gpio = build_gpio_chardev("gpiochip0")
    my_gpio.config_by_board_rev()
    await my_gpio.setup()

    my_gpio.set_button_light(blue=True)
    await asyncio.sleep(2)
    my_gpio.set_button_light(red=True)
    await asyncio.sleep(2)
    my_gpio.set_button_light(green=True)
    await asyncio.sleep(2)

asyncio.run(main())
