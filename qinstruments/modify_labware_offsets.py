# For labware that is mounted on a custom device: create a new labware
# definition that is a modification of an existing Opentrons definition

import sys
import json
import os

from opentrons.protocols import labware


DEVICE_NAME = "bioshake"
# How much the device "offsets" the labware in xyz
DEVICE_X = -3.577
DEVICE_Y = 3.665
DEVICE_Z = 63


# Function so this can be imported and used as a Python module
def modify_labware(labware_name):

    # Get this labware definition as a dictionary
    lab_dict = labware.get_labware_definition(lab_name)

    # Make modifications
    lab_name_mod = "{}_on_{}".format(lab_name, DEVICE_NAME)

    lab_dict['cornerOffsetFromSlot']['x'] = DEVICE_X
    lab_dict['cornerOffsetFromSlot']['y'] = DEVICE_Y
    lab_dict['cornerOffsetFromSlot']['z'] = DEVICE_Z
    lab_dict['metadata']['displayName'] = lab_name_mod

    return lab_dict


# If run standalone, creates a new JSON definition
if __name__ == "__main__":

    # Set parameters
    if len(sys.argv) != 2:
        print("Usage: labware_modifier_standalone <opentrons_labware_name>")
        sys.exit()

    # Opentrons labware definition name, e.g.
    # opentrons_15_tuberack_nest_15ml_conical
    lab_name = sys.argv[1]

    lab_name_mod = "{}_on_{}".format(lab_name, DEVICE_NAME)
    lab_dict_mod = modify_labware(labware_name=lab_name)

    # Write the modified labware definition to a new JSON file
    out_path = os.path.join(os.getcwd(), "{}.json".format(lab_name_mod))
    with open(out_path, "w") as fw:
        fw.write(json.dumps(lab_dict_mod))

    print("Labware definition written to file: {}".format(out_path))
