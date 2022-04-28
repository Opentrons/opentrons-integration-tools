import serial


class BioshakeDriver():
    def __init__(self, my_device_name="/dev/ttyUSB0"):
        # Default Bioshake device name is /dev/ttyUSB0
        # If multiple Bioshakes are connected, you will need to find which
        # device uses which device file (ttyUSB0, ttyUSB1...)
        # (See "serial-device/ttyusb_devices.py")
        DEVICE_NAME = my_device_name
    
        # Specified in the QInstruments documentation
        BAUDRATE = 9600
        BYTESIZE = serial.EIGHTBITS
        PARITY = serial.PARITY_NONE
        STOPBITS = serial.STOPBITS_ONE

        # Optional timeouts in seconds
        READ_TIMEOUT = 2
        WRITE_TIMEOUT = 2

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

    def get_info(self):
        self._send_command("info")

        info = self._read_response()

        return info

    def home_shaker(self):
        self._send_command("shakeGoHome")

    def set_shake(self, my_rpm, my_shake_time):
        rpm = str(my_rpm)
        shake_time = str(my_shake_time)

        self._send_command("ssts{}".format(rpm))
        self._send_command("shakeOnWithRuntime{}".format(shake_time))

    def temp_on(self, my_temp):
        temp = float(my_temp)*10
        temp = int(temp)
        temp = str(temp)

        self._send_command("setTempTarget{}".format(temp))
        self._send_command("tempOn")

    def temp_off(self):
        self._send_command("tempOff")

    def unlock(self):
        self._send_command("setElmUnlockPos")

    def lock(self):
        self._send_command("setElmLockPos")
