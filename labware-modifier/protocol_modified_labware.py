from opentrons import protocol_api
import os
import sys

sys.path.append("/var/lib/jupyter/notebooks")
import labware_modifier


metadata = {
    'protocolName': 'Use labware_modifier Module',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Loads labware that has been modified',
    'apiLevel': '2.12'
}


def run(ctx):

    # Load tip rack
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 10)

    # Load plate with predefined offsets
    plate_x = 5
    plate_y = -5
    plate_z = 50
    labware_with_offsets = labware_modifier.set_labware_offsets(
        "biorad_96_wellplate_200ul_pcr", plate_x, plate_y, plate_z)
    plate = ctx.load_labware_from_definition(labware_with_offsets, 5)

    # Load pipette
    p300 = ctx.load_instrument("p300_single", "right", tip_racks=[tip_rack])

    p300.pick_up_tip()

    p300.move_to(plate["A1"].top())

    p300.drop_tip()
