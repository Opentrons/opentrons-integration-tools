# Helps find attached ttyUSB<> devices in /dev/
# Returns a dict of {serial_number: device_name}
# If the devices aren't found, you may need to unplug and plug them in again

import subprocess
import re
import os


def get_usb_devices():

    out_bytes = subprocess.check_output("dmesg")
    out_string = out_bytes.decode()

    # Each message "block" is a new device detected
    out_split = re.split("New USB device found", out_string)
    list_len = len(out_split)

    # The dict of serial number: device name
    dev_dict = {}

    # Start at the last message block, go back: you want the most recent dmesg
    # entries
    # Discard the 0th block (before first USB device detected)
    for c in range(list_len-1, 0, -1):

        # Current message block
        b = out_split[c]

        # A block with a USB device will have serial number AND device name
        if "now attached to" in b and "SerialNumber" in b:

            # Split message block by line
            block_split = b.split("\n")

            # Go through each line in the block, get serial number and device
            # name
            for s in block_split:

                if "SerialNumber:" in s:
                    serial_block = s.split()
                    serial_number = serial_block[len(serial_block) - 1]

                if "now attached to" in s:
                    device_name_block = s.split()
                    device_name = device_name_block[len(device_name_block) - 1]

            # Back to current block
            if (serial_number not in dev_dict.keys() and
                device_name not in dev_dict.values()):
                dev_dict[serial_number] = device_name

    # Filter dict for current devices connected (remove historical data)
    disconnected_devices = []

    dev_dir = "/dev/"
    for s in dev_dict:
        dev_file = os.path.join(dev_dir, dev_dict[s])
        if not os.path.exists(os.path.join(dev_dir, dev_dict[s])):
            disconnected_devices.append(s)

    for e in disconnected_devices:
        dev_dict.pop(e)

    return dev_dict


# Usage example
if __name__ == "__main__":

    my_serial_no = "abc123"
    my_devices = get_usb_devices()
    # This will be "/dev/ttyUSB<>"
    device0 = os.path.join("/dev/", my_devices[my_serial_no])
