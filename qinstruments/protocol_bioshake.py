# Protocol for BioShake 3000-T ELM with QOT adapter

import sys
import serial

from opentrons import protocol_api

# Python modules that have been uploaded to the Jupyter notebook
sys.path.append("/var/lib/jupyter/notebooks/")
import bioshake
import modify_labware_offsets


metadata = {
    'protocolName': 'Protocol Bioshake',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Use QInstruments BioShake with serial driver',
    'apiLevel': '2.12'
}


def bioshake_action(ctx):
    ctx.comment("Bioshake action function")

    # See bioshake.py
    my_bioshake = bioshake.BioshakeDriver()
    my_bioshake.unlock()
    ctx.delay(2)
    my_bioshake.lock()
    ctx.delay(2)

    # Not blocking, wait for action to complete
    my_bioshake.set_shake(1000, 5)
    ctx.delay(6)


def run(ctx):
    # Load tip rack
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 5)

    # Load well plate that is on BioShake using the BioShake's geometry
    # (see "labware-modifier")
    labware_with_offsets = modify_labware_offsets.modify_labware(
        "nest_96_wellplate_2ml_deep")
    plate = ctx.load_labware_from_definition(labware_with_offsets, 10)

    # Load pipette
    p300 = ctx.load_instrument("p300_single_gen2", "left",
                               tip_racks=[tip_rack])

    p300.pick_up_tip()

    p300.move_to(plate['A1'].top())

    if not ctx.is_simulating():
        bioshake_action(ctx)

    p300.return_tip()
