# Get the event file of an external camera plugged into the OT-2 (usable by ffmpeg)

import os


def find_camera():

	V4L_DIR = "/dev/v4l/by-id"
	OT_CAMERA = "usb-H264_USB_Camera"

	# Get symbolic links for the attached cameras from Video4Linux dir
	camera_list = os.listdir(V4L_DIR)

	for c in camera_list:
		if OT_CAMERA not in c:

			# Follow the symbolic link to get the event file
			camera_rel_path = os.readlink(os.path.join(V4L_DIR, c))
			camera_full_path = os.path.join("/dev", camera_rel_path.lstrip("/."))
			print("External camera found: {}".format(camera_full_path))
			return camera_full_path

	print("External camera not found, defaulting to OT-2 camera")
	return "/dev/video0"
