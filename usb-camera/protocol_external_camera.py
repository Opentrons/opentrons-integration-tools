from opentrons import protocol_api
import os
import subprocess

metadata = {
    'protocolName': 'Protocol External Camera',
    'author': 'Opentrons <protocols@opentrons.com>',
    'description': 'Takes a photo with an external camera and puts it in Jupyter notebook',
    'apiLevel': '2.11'
}


OT_CAMERA = "usb-H264_USB_Camera"

OT_LABWARE = "opentrons_96_tiprack_300ul"
OT_LABWARE_SLOT = 5
OT_PIPETTE = "p300_single_gen2"
OT_PIPETTE_MOUNT = "right"

JUPYTER_PATH = "/var/lib/jupyter/notebooks"
PHOTO_NAME = "photo0.jpg"
DEBUG_NAME = "photo_debug.txt"


def find_camera():

    v4l_dir = "/dev/v4l/by-id"

    debug_file = open((os.path.join(JUPYTER_PATH, DEBUG_NAME)), "w")

    # Get symbolic links for the attached cameras from Video4Linux dir
    camera_list = os.listdir(v4l_dir)

    for c in camera_list:

        # Follow the symbolic link to get the event file
        camera_rel_path = os.readlink(os.path.join(v4l_dir, c))
        camera_full_path = os.path.join("/dev", camera_rel_path.lstrip("/."))

        debug_file.write("{}\n{}\n{}\n".format(c, camera_rel_path, camera_full_path))

        # Find camera that is not Opentrons camera
        if OT_CAMERA not in c:

            debug_file.write("External camera found")
            debug_file.close()
            return camera_full_path

    debug_file.write("External camera NOT found")
    debug_file.close()
    return "/dev/video0"


def run(ctx):

    # Load Labware
    tip_rack = ctx.load_labware(OT_LABWARE, OT_LABWARE_SLOT)
    p300 = ctx.load_instrument(OT_PIPETTE, OT_PIPETTE_MOUNT,
                               tip_racks=[tip_rack])

    # Get camera
    my_camera = find_camera()

    p300.pick_up_tip()

    # Take a photo
    my_photo = os.path.join(JUPYTER_PATH, PHOTO_NAME)
    subprocess.check_output(["ffmpeg", "-y", "-f", "video4linux2", "-i", my_camera, "-frames", "1", my_photo])

    p300.drop_tip()
