from opentrons import protocol_api

import gspread


metadata = {
    'protocolName': 'Variable Distribute: Google Spreadsheet API',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Distributes to a variable number of wells',
    'apiLevel': '2.13'
}


# See gspread documentation
CREDENTIALS_FILE = "/var/lib/jupyter/notebooks/google_credentials.json"
SPREADSHEET_KEY = ""


# Get number of samples from your spreadsheet
def get_num_samples():

    gc = gspread.service_account(filename=CREDENTIALS_FILE)
    sh = gc.open_by_key(SPREADSHEET_KEY)

    # Different ways to get value of cell A1
    #sh_value = sh.sheet1.get("A1").first()
    #sh_value = sh.sheet1.cell(1, 1).value
    sh_value = sh.sheet1.acell("A1").value

    # gspread returns a string, have to convert to int
    num_samples = int(sh_value)

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
