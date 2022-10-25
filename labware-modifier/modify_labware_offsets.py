import os
import json


def set_labware_offsets(labware_name, x, y, z):
    """
    labware_name: either the Opentrons labware API name, or custom 
                  labware file path
    x, y, z: offsets in mm
    
    returns: labware definition dict used by "load_labware_by_definition()"
    """

    if ".json" in labware_name:
        labware_file = labware_name
    else:
        # An Opentrons labware definition is stored in the file:
        # <ot2_labware_path> / <labware API name> / "1.json"
        ot2_labware_path = "/usr/lib/python3.7/site-packages/opentrons_shared_data/data/labware/definitions/2/"
        labware_file = os.path.join(ot2_labware_path, labware_name, "1.json")

    with open(labware_file, "r") as f:

        def_with_offsets = json.load(f)

        # Modify the labware definition dict with your offsets
        def_with_offsets['cornerOffsetFromSlot']['x'] = x
        def_with_offsets['cornerOffsetFromSlot']['y'] = y
        def_with_offsets['cornerOffsetFromSlot']['z'] = z

        return def_with_offsets
