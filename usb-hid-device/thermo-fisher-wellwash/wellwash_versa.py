"""
PyUSB driver for the Thermo Fisher Wellwash Versa
Based on "Thermo Scientific Wellwash Versa Remote Control Command Sets r1.0"
"""

import time

import usb.core
import usb.backend.libusb1


# Specified in device documentation
USB_VENDOR_ID = 0x0AB6
USB_PRODUCT_ID = 0x0888
READ_ENDPOINT = 0x81
WRITE_ENDPOINT = 0x01


class WellwashDriver:

	def __init__(self):
		# Have to specify the backend on the OT-2, not automatically found
		self.backend = usb.backend.libusb1.get_backend(
			find_library=lambda x: "/usr/lib/libusb-1.0.so")

		self.dev = usb.core.find(
			idVendor=USB_VENDOR_ID,
			idProduct=USB_PRODUCT_ID,
			backend=self.backend
			)

		if self.dev.is_kernel_driver_active(0) == True:
			self.dev.detach_kernel_driver(0)

		self.dev.set_configuration()

		# 30 seconds
		self.timeout = 30000

	def cleanup(self):
		"""
		Reset the device, which may prevent errors across runs
		"""
		self.dev.reset()

	def _send_command(self, my_command):
		"""
		Worker function: format the command for the Wellwash and send it
		"""
		command_message = f"{my_command}\r\n".encode(encoding="ascii")
		self.dev.write(WRITE_ENDPOINT, command_message, self.timeout)

	def _read_response(self):
		"""
		Worker function: read a response from the Wellwash
		"""
		# Put the buffer time here
		time.sleep(1)
		buf_len = 64
		r = self.dev.read(READ_ENDPOINT, buf_len, self.timeout)
		return r

	def get_version(self):
		self._send_command("VER")
		version = self._read_response()
		return version

	def buzzer(self, ui_frequency, ui_time):
		buzz_command = f"BEE {ui_frequency} {ui_time}"
		self._send_command(buzz_command)

	def start_protocol(self, a_protocol_name):
		protocol_command = f"BGN {a_protocol_name}"
		self._send_command(protocol_command)
		protocol_response = self._read_response()
		return protocol_response

	def abort(self):
		# Hex 1b is the ASCII value for ESC (escape)
		abort_command = "\x1b"
		self._send_command(abort_command)
		abort_response = self._read_response()
		return abort_response

	def list_protocol_channels(self):
		self._send_command("LPC")
		channels = self._read_response()
		return channels

	def list_protocols(self):
		self._send_command("PLI")
		protocols = self._read_response()
		return protocols


if __name__ == "__main__":

	my_washer = WellwashDriver()

	print(my_washer.get_version())

	my_washer.buzzer(500, 3000)
	time.sleep(2)
	my_washer.buzzer(800, 1000)
	time.sleep(2)

	print(my_washer.list_protocols())
