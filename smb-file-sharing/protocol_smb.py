import sys
import os

from opentrons import protocol_api

sys.path.append("/var/lib/jupyter/notebooks/")
import ot_smb


metadata = {
    'protocolName': 'Variable Distribute: SMB',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Distributes to a variable number of wells',
    'apiLevel': '2.13'
}


# The name and path of the file on the remote server
REMOTE_PATH = "/num_samples.txt"
# How the file will be saved to the Opentrons robot
LOCAL_PATH = "/var/lib/jupyter/notebooks/num_samples.txt"


# Get file that contains number of samples
def get_num_samples():

    ot_smb.smb_get_file(remote_path=REMOTE_PATH, local_path=LOCAL_PATH)

    with open(LOCAL_PATH, "r") as f:
        num_samples = int(f.read())

    # Not error-checked (needs to be between 1-24)
    return num_samples


def run(ctx):

    # Load labware and pipettes
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 9)
    reservoir = ctx.load_labware("nest_12_reservoir_15ml", 6)
    plate = ctx.load_labware("corning_24_wellplate_3.4ml_flat", 4)
    p300 = ctx.load_instrument("p300_single_gen2", "right",
                               tip_racks=[tip_rack])

    # Get number of samples
    num_samples = get_num_samples()

    # Transfer based on number of samples
    dest_wells = []
    for i in range(0, num_samples):
        dest_wells.append(plate.wells()[i])

    p300.distribute(50, reservoir["A1"], dest_wells, new_tip="once")
