"""
The USB Xbox 360 controller is a good device to test USB-HID communication. It
obviously has different buttons that produce different input values, and it
can also receive signals to change the LEDs and activate the rumble.

More details about the Xbox 360 controller HID specification:
partsnotincluded.com/understanding-the-xbox-360-wired-controllers-usb-data/
"""

import array

import usb.core
import usb.backend.libusb1


USB_VENDOR_ID = 0x045e
USB_PRODUCT_ID = 0x028e

READ_ENDPOINT = 0x81
WRITE_ENDPOINT = 0x01

# 30 seconds
TIMEOUT = 30000

"""
Button inputs:

1 = LB (left bumper)
2 = RB (right bumper)
16 = A
32 = B
64 = X
128 = Y

The other buttons and joysticks are more complicated to implement
"""
VALID_INPUTS = [1, 2, 16, 32, 64, 128]

"""
LED commands:

6 = Player 1 on
7 = Player 2 on
8 = Player 3 on
9 = Player 4 on
10 = Rotating
13 = Alternating
"""
VALID_COMMANDS = [6, 7, 8, 9, 10, 13]


class Xbox360ControllerDriver:

	def __init__(self):
		self.backend = usb.backend.libusb1.get_backend(
			find_library=lambda x: "/usr/lib/libusb-1.0.so")

		self.dev = usb.core.find(
			idVendor=USB_VENDOR_ID,
			idProduct=USB_PRODUCT_ID,
			backend=self.backend)

		if self.dev.is_kernel_driver_active(0) == True:
			self.dev.detach_kernel_driver(0)

		self.dev.set_configuration()

		self.timeout = TIMEOUT

	def send_command(self, my_command):
		"""
		Change the LED pattern on the Xbox 360 controller
		"""
		if my_command in VALID_COMMANDS:
			command_message = array.array('B', [1, 3, my_command])
			self.dev.write(WRITE_ENDPOINT, command_message, self.timeout)

	def read_input(self):
		"""
		Determine if one of these Xbox 360 controller buttons was pressed:
		Left bumper, right bumper, A, B, X, Y
		"""
		event_len = 20
		read_loc = 3

		# Arbitrary value for invalid command
		input_val = -1

		loop = True
		while loop == True:
			try:
				r = self.dev.read(READ_ENDPOINT, event_len, self.timeout)

				if len(r) == event_len and r[read_loc] in VALID_INPUTS:
					input_val = r[read_loc]
					loop = False

			except usb.core.USBTimeoutError:
				loop = False

		return input_val

	def cleanup(self):
		"""
		Reset the device, which may prevent errors across runs
		"""
		self.dev.reset()

if __name__ == "__main__":
	"""
	Test loop: pressing A, B, X, Y, or LB activates a different LED pattern
	Pressing RB exits
	"""

	my_controller = Xbox360ControllerDriver()

	while True:
		b = my_controller.read_input()

		if b == 16:
			my_controller.send_command(6)
		elif b == 32:
			my_controller.send_command(7)
		elif b == 64:
			my_controller.send_command(8)
		elif b == 128:
			my_controller.send_command(9)
		elif b == 1:
			my_controller.send_command(10)
		else:
			break

	my_controller.cleanup()
