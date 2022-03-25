# Integrating a USB HID-Class Device

### Introduction
Many USB devices use the HID specification:

https://en.wikipedia.org/wiki/USB_human_interface_device_class

In the context of the OT-2, which is a Linux system, this means that the OS recognizes and communicates with the device in a predictable way, and may already have a generic driver for it. This allows for an easier and more robust integration than is possible with a lower-level serial device.

There are many ways to work with USB HID in Linux, but since the OT-2's software stack is mostly in Python, it is easiest to use a high-level Python library.

### Using PyUSB
PyUSB is 100% written in Python and available on PyPI, making it easier to use on the OT-2 than other options. You can install it on the robot with `pip install pyusb`, and its dependencies are already present.

There is a detailed tutorial that covers connecting to a device and multiple usage scenarios:

https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst

Some highlights:

* You will need the USB Vendor ID and USB Product ID of the device, which can be found by running `lsusb` in Linux (it should also be provided by the manufacturer in the user manual or integration guide)
* On the OT-2, you need to manually specify the USB backend, which looks like this: `backend = usb.backend.libusb1.get_backend(find_library=lambda x: "/usr/lib/libusb-1.0.so")`
* If you get a `Resource busy` error when trying to communicate with the device, that means that Linux already has a driver for it and it is communicating with the kernel. You will need to detach the kernel driver: `dev.detach_kernel_driver(0)`
* It may be necessary to reset the device in between program runs with `dev.reset()`, especially if the driver is being used across different Python contexts (e.g. Protocol, Jupyter, script run by SSH)
