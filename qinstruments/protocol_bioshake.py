import sys
import serial

from opentrons import protocol_api

# Python modules that have been uploaded to the Jupyter notebook
# (bioshake.py, labware_modifier.py)
sys.path.append("/var/lib/jupyter/notebooks/")
import bioshake
import labware_modifier


metadata = {
    'protocolName': 'Protocol Bioshake',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Use QInstruments Bioshake with serial driver',
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

    # Load well plate that is on Bioshake using the Bioshake's geometry
    # (see "labware-modifier")
    # These specific numbers are for Bioshake 3000-T ELM with QOT adapter
    bioshake_x = -3.577
    bioshake_y = 3.665
    bioshake_z = 63
    labware_with_offsets = labware_modifier.set_labware_offsets(
        labware_name = "nest_96_wellplate_2ml_deep",
        x = bioshake_x,
        y = bioshae_y,
        z = bioshake_z)
    plate = ctx.load_labware_from_definition(labware_with_offsets, 10)

    # Load pipette
    p300 = ctx.load_instrument("p300_single_gen2", "left",
                               tip_racks=[tip_rack])

    p300.pick_up_tip()

    p300.move_to(plate['A1'].top())

    if not ctx.is_simulating():
        bioshake_action(ctx)

    p300.return_tip()
