from opentrons import protocol_api
from evasdk import Eva


# Set your IP address and token here
AUTOMATA_IP = "192.168.0.207"
AUTOMATA_TOKEN = ""


metadata = {
    'protocolName': 'Automata Toolpath',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Move the Automata Eva with toolpaths',
    'apiLevel': '2.12'
}


# Run two toolpaths in a row
# This could also be split into different functions
def automata_action(ctx):

    my_eva = Eva(AUTOMATA_IP, AUTOMATA_TOKEN)

    with my_eva.lock():

        # Load toolpaths that were created before, knowing their IDs
        tp0 = my_eva.toolpaths_retrieve(0)
        tp1 = my_eva.toolpaths_retrieve(1)

        # Run the first toolpath once
        ctx.comment("Automata toolpath 0")
        my_eva.control_wait_for_ready()

        my_eva.toolpaths_use(tp0)
        my_eva.control_home()
        my_eva.control_run(loop=1)
        my_eva.control_home()

        ctx.delay(seconds=5)

        # Run the second toolpath once
        ctx.comment("Automata toolpath 1")
        my_eva.control_wait_for_ready()

        my_eva.toolpaths_use(tp1)
        my_eva.control_home()
        my_eva.control_run(loop=1)
        my_eva.control_home()


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
