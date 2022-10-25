# Shows where the labware definition JSON files are stored on the robot file
# system or in the app's Python folder

import sys
import os
import json

from opentrons_shared_data import get_shared_data_root
from opentrons.protocols.api_support.constants import STANDARD_DEFS_PATH
from opentrons.protocols import labware


defs_path = os.path.join(get_shared_data_root(), STANDARD_DEFS_PATH)
print("Definitions path:\n{}\n".format(defs_path))

print("All labware definition files:")
defs_list = labware.get_all_labware_definitions()
for l in defs_list:
    lab_path = os.path.join(defs_path, l, "1.json")
    print(lab_path)
