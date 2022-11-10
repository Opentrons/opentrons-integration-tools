from opentrons import protocol_api


metadata = {
    "protocolName": "Wait for Button",
    "author": "Opentrons <protocols@opentrons.com>",
    "description": "Pause at a specified step, resume with button press",
    "apiLevel": "2.12"
}


def wait_for_button(ctx, hw_api, timeout):

    for _ in range(0, timeout):

        log_msg = f"Waiting for button press. Timeout = {timeout} seconds."
        ctx.delay(seconds=1, msg=log_msg)

        # True if button is pressed, False if not
        button_status = hw_api._backend.gpio_chardev.read_button()
        if button_status is True:
            break


def run(ctx: protocol_api.ProtocolContext):

    # Protocol setup
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 11)
    p300 = ctx.load_instrument("p300_single_gen2", "right",
                               tip_racks=[tip_rack])

    # Hardware Control API setup
    unsafe_hardware_api = ctx._hw_manager.hardware
    button_timeout = 60

    # Begin protocol
    p300.move_to(tip_rack['A1'].top())

    # Pause here and wait for button press
    if not ctx.is_simulating():
        wait_for_button(ctx, unsafe_hardware_api, button_timeout)

    # Continue protocol
    p300.pick_up_tip()
    p300.drop_tip()
