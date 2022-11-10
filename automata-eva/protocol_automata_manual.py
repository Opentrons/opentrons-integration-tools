from opentrons import protocol_api
from evasdk import Eva


# Set your IP address and token here
AUTOMATA_IP = "192.168.0.207"
AUTOMATA_TOKEN = ""


metadata = {
    'protocolName': 'Automata Manual',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Move the Automata Eva manually',
    'apiLevel': '2.12'
}


def automata_action(ctx):

    ctx.comment("Automata action function")

    my_eva = Eva(AUTOMATA_IP, AUTOMATA_TOKEN)

    pos_home = [0, 0.85, -2.5, 0.02, -1.5, 0]
    pos_extended = [0.5, 0.85, -2.5, 0.02, -1.5, 0]

    control_speed = 0.1
    control_mode = "teach"

    with my_eva.lock():
        my_eva.control_wait_for_ready()

        my_eva.control_go_to(
            pos_home,
            wait_for_ready=True,
            max_speed=control_speed,
            mode=control_mode)

        my_eva.control_go_to(
            pos_extended,
            wait_for_ready=True,
            max_speed=control_speed,
            mode=control_mode)

        my_eva.control_go_to(
            pos_home,
            wait_for_ready=True,
            max_speed=control_speed,
            mode=control_mode)


def run(ctx):

    # Load labware and pipette
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 9)
    p300 = ctx.load_instrument("p300_single_gen2", "right",
                               tip_racks=[tip_rack])

    # Opentrons action
    p300.move_to(tip_rack['A1'].top())

    # Automata action
    if not ctx.is_simulating():
        automata_action(ctx)

    # Opentrons action
    p300.pick_up_tip()
    p300.drop_tip()
