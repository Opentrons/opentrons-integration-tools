# Integrating a Barcode Scanner

### Introduction
The OT-2 runs a Jupyter Notebook server providing a web-based, interactive computing platform that can be accessed at [IP address of your OT-2]:48888 (or by clicking "OPEN" in the OT app). This interface can be used to execute a python loop (module_barcodescanning.py) to solicit input directly from the user (e.g.- deck location, labware definition files, preference to scan in column-wise or row-wise order), read scan results, display them to the user, and then write each approved scan result along with user inputs to scans.csv so that when scanning is finished the barcode and associated data (deck location, well etc.) can be read directly as csv input by a python protocol about to be dropped into the OT app without the need to manually upload or manage the input file (it is possible to manually download, edit, or upload scans.csv but this is not required - it is recommended to let the code write and manage the file).

### Integration Summary
If your barcode scanner is operating in USB-HID mode, you can simply plug it in to the Raspberry Pi via USB (after the OT-2 has fully booted) and it's device file at `/dev/hidraw0` will be read by the scanning loop. module_barcodescanning.py, click_here_to_run_scanning_loop.ipynb, and labware definition .json files can be uploaded to the OT-2 Jupyter Notebook with the upload button in the Jupyter interface. Open click_here_to_run_scanning_loop.ipynb and click "run" to initiate the scanning loop.

### Files

* module_barocdescanning.py contains the python code for the scanning loop.

* click_here_to_run_scanning_loop.ipynb is a Jupyter Notebook file containing a single line of code (%run module_barcodescanning.py) used to execute the scanning module and render the display within a single Jupyter code cell.

* 32Tuberack15mlFalcontube.json is an example labware definition file containing information about the spatial layout and wells of the labware containing the samples to be scanned.

* example_protocol.py shows how a python API protocol can run the OT-2 using the OT app and scans.csv as csv input.

### List of Scanners that are Known to be Compatible
* [Tera 1D Wired Barcode Scanner Model: L5100Y](https://tera-digital.com/products/tera-laser-barcode-scanner-usb-wired-1d-handheld) To configure the scanner - user can scan barcodes found in the user manual to choose the following settings: interface: USB-HID mode, scan mode: manual trigger mode, terminator: CR

### Scanning Interface
![scanning interface](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/barcodescanning/interface0130.png)


### Scans CSV
![scans csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/barcodescanning/scans_csv.png)
