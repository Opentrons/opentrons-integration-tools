from opentrons import protocol_api
import os
import sys

sys.path.append("/var/lib/jupyter/notebooks")
import modify_labware_offsets


metadata = {
    'protocolName': 'Use modify_labware_offsets Module',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Loads a modified labware definition',
    'apiLevel': '2.12'
}


def run(ctx):

    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 10)
    p300 = ctx.load_instrument("p300_single", "right", tip_racks=[tip_rack])

    # Load labware that is on custom device
    labware_with_offsets = modify_labware_offsets.modify_labware(
        "biorad_96_wellplate_200ul_pcr")
    plate = ctx.load_labware_from_definition(labware_with_offsets, 5)

    p300.pick_up_tip()
    p300.move_to(plate["A1"].top())
    p300.drop_tip()
