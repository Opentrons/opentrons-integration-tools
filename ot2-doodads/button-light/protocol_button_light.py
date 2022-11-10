from opentrons import protocol_api


metadata = {
    "protocolName": "Protocol Button Light",
    "author": "Opentrons <protocols@opentrons.com>",
    "description": "Change button light color in a protocol",
    "apiLevel": "2.12"
}


def run(ctx):

    # Protocol setup
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 11)
    p300 = ctx.load_instrument("p300_single_gen2", "right",
                               tip_racks=[tip_rack])

    # Hardware Control API setup
    unsafe_hardware_api = ctx._hw_manager.hardware

    unsafe_hardware_api._backend.gpio_chardev.set_button_light(green=True)
    p300.move_to(tip_rack['A1'].top())
    ctx.delay(seconds=1)
    unsafe_hardware_api._backend.gpio_chardev.set_button_light(red=True)
    ctx.delay(seconds=1)

    # Change to blue at the end of a protocol, or the last color will remain
    unsafe_hardware_api._backend.gpio_chardev.set_button_light(blue=True)
