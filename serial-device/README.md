# Integrating a Serial Device

### Introduction
Some third-party modules are controlled with low-level serial communication: e.g. Arduino-based devices. To use one of these devices with the OT-2 in a protocol, you can plug the device into one of the robot's USB ports use the `pySerial` library, which is already included.

If the module is on the deck, remember to define and load it as labware so that the robot doesn't collide with it!

### pySerial Documentation
https://pyserial.readthedocs.io/en/latest/pyserial.html
