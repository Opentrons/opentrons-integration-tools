# QInstruments Devices

There are currently two ways to use QInstruments devices in Opentrons protocols.

### 1 - QOT Kit

QInstruments provides a detailed integration that includes a Python library and labware definitions. This is all well-documented here:

https://www.qinstruments.com/knowledge/qinstruments-supports-opentrons-applications/

You will need an FTDI RS232 to USB adapter that is programmed with "QInstruments" as the "Manufacturer" property (see "EEPROM programming utility..." link on the website).

### 2 - Serial Driver

The other option is to directly communicate with the device via serial. This works with any RS232 to USB adapter; there is no need to specially program it.

"bioshake.py" is an [example serial driver](https://github.com/Opentrons/opentrons-integration-tools/tree/main/serial-device) for the QInstruments BioShake. It is based on and can be expanded using the QInstruments integration manual:

https://www.qinstruments.com/fileadmin/Article/All/integration-manual-en-1-8-0.pdf

"protocol_bioshake.py" is an example protocol that uses a BioShake on the OT-2 deck. It uses the "bioshake.py" driver (`import bioshake`) to send commands to the device, and the [labware_modifier](https://github.com/Opentrons/opentrons-integration-tools/tree/main/labware-modifier) utility to give the OT-2 the correct geometry of the labware+BioShake. It performs all of the BioShake functionality in a dedicated function, `bioshake_action()`, for convenience, but it be done in the main `run()` function as well.
