# Example serial driver that can be extended and used in an Opentrons protocol

import serial


# This value may need to be found through trial and error
DEVICE_NAME = "/dev/ttyUSB0"

# These values should be in the device documentation
BAUDRATE = 9600
BYTESIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE

# Optional timeouts in seconds
READ_TIMEOUT = 0.5
WRITE_TIMEOUT = 0.5


class SerialDriver():
    def __init__(self):

        self.serial_object = serial.Serial(
            port=DEVICE_NAME,
            baudrate=BAUDRATE,
            bytesize=BYTESIZE,
            parity=PARITY,
            stopbits=STOPBITS,
            timeout=READ_TIMEOUT,
            write_timeout=WRITE_TIMEOUT)

    def _reset_buffers(self):
        """
        Worker function
        """
        self.serial_object.reset_input_buffer()
        self.serial_object.reset_output_buffer()

    def _read_response(self):
        """
        Worker function
        """
        output_lines = self.serial_object.readlines()
        output_string = ""

        for l in output_lines:
            output_string += l.decode("utf-8")

        return output_string

    def _send_command(self, my_command):
        """
        Worker function
        """
        SERIAL_ACK = "\r\n"

        command = my_command
        command += SERIAL_ACK

        self.serial_object.write(command.encode())
        self.serial_object.flush()

    def example_driver_function(self):
        """
        Use the worker functions to build the driver functionality
        """
        self._send_command("dostuff")

        info = self._read_response()

        return info
