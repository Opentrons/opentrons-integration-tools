# Example serial driver that can be extended and used in an Opentrons protocol

import serial


BAUDRATE = 9600
DEVICE_FILE = "/dev/ttyUSB0"
TIMEOUT = 2


class SerialDriver():
    def __init__(self):
        self.baudrate = BAUDRATE
        self.device_file = DEVICE_FILE

        self.port = serial.Serial(
            self.device_file, self.baudrate, timeout=TIMEOUT)

    def _reset_buffers(self):
        """
        Worker function
        """
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()

    def _read_response(self):
        """
        Worker function
        """
        output_lines = self.port.readlines()
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

        self.port.write(command.encode())
        self.port.flush()

    def example_driver_function(self):
        """
        Use the worker functions to build the driver functionality
        """
        self._send_command("dostuff")

        info = self._read_response()

        return info
