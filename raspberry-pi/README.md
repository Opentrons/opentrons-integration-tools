# Setting Up a Raspberry Pi for Robot Simulation

### Introduction
There are many cases where it is advantageous to do development and testing for the OT-2 without using a robot. One option is running the Robot Server in simulation or emulation mode:

https://github.com/Opentrons/opentrons/tree/edge/robot-server#simulators

However, its functionality is limited. Using a Raspberry Pi with the OT-2 OS installed gives you an experience that is much closer to working with a "real" robot. Some advantages:
* Access to the robot's file system, and therefore SSH/SCP
* The ability to install new software packages
* The ability to plug in USB devices

### Hardware Requirements
* Raspberry Pi 3 Model B or B+
* Micro SD card 16 GB or greater
* Ethernet cable

### Part 1: OS and Network Setup
1. Flash the OT-2 OS onto the SD card by following these instructions (skip the "Next steps" section): https://support.opentrons.com/s/article/Reflashing-the-OT-2-s-SD-card
2. Connect the Raspberry Pi to your computer via Ethernet
3. Open the Opentrons app and find the IP address of the Pi by looking at the yellow "Unable to establish connection" message (note: this message appears because there is no robot hardware is connected to the Pi, so the OS thinks that there is a hardware failure)
4. Use that IP address to set up SSH by following these instructions: https://support.opentrons.com/s/article/Setting-up-SSH-access-to-your-OT-2

### Part 2: Configure the Simulated Hardware
1. Create a JSON file that contains your desired hardware setup: https://github.com/Opentrons/opentrons/tree/edge/robot-server/simulators
   - It may be easiest to download "test.json" from this link and modify it
2. SCP this file to the "/data/" folder of the Raspberry Pi

### Part 3: Configure the Robot Server
1. SSH into the Raspberry Pi
2. Create this file: "/data/robot.env", and add the lines:
   - `ENABLE_VIRTUAL_SMOOTHIE=1`
   - `RUNNING_ON_PI=0`
   - `OT_ROBOT_SERVER_simulator_configuration_file_path=/data/<your JSON file from Part 2>`
3. Reboot the Pi
4. After a few minutes, you should be able to "Connect" to the Pi in the app. Now you can calibrate the deck and pipettes as if you were using a real robot, and start uploading protocols!

### Limitations
* Can't run protocols via Jupyter or SSH (`opentrons.execute` calls `build_hardware_controller()`, which requires a real hardware controller)
* `ProtocolContext.is_simulating()` is always true (not just in the analysis phase like on a real OT-2), making it not useful
