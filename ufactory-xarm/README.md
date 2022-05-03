# UFACTORY xArm

### Introduction

The UFACTORY xArm series can be easily controlled by the OT-2 in a protocol thanks to the Python SDK provided by UFACTORY. There are just a few one-time setup steps to get started.

### Hardware Requirements
* UFACTORY xArm
* UFACTORY gripper (optional)
* Ethernet-USB adapter
* Tape (optional)

Opentrons has tested the xArm 6 and Biogripper, but the other xArm arms and grippers should be compatible with this setup.

### Hardware Setup
1. Set up the UFACTORY arm, gripper, and control box according to the UFACTORY instructions
2. Plug an Ethernet cable into the xArm control box
3. Plug the other end of the Ethernet cable into your Ethernet-USB adapter
4. Plug the adapter into any of the OT-2's USB ports
   - You may want to tape the Ethernet cable to the side or top of the OT-2 so that it doesn't go over the deck, depending on where the control box is relative to the OT-2.
   - Unfortunately it is not possible to connect the OT-2 (or any computer) and the xArm directly via Wi-Fi. It is possible to connect the control box to your Wi-Fi router via Ethernet, which allows you to control the arm wirelessly, but this is not recommended by UFACTORY because of possible information loss. Also, this may cause other unexpected issues with your network, and most likely your Wi-Fi router is not physically located somewhere where this kind of connection is convenient.

### Software Setup
**Part 1: Install the UFACTORY SDK**
1. Download the latest version of the xArm Python SDK as a .zip ("Code" → "Download ZIP"): [xArm-Python-SDK](https://github.com/xArm-Developer/xArm-Python-SDK)
2. Download the "ot-ufactory-install.ipynb" Jupyter notebook
3. Upload the “xArm-Python-SDK-master.zip” file and the notebook to the OT-2's Jupyter notebook folder: [Uploading files through Jupyter Notebook](https://support.opentrons.com/s/article/Uploading-files-through-Jupyter-Notebook)
4. Run the "ot-ufactory-install.ipynb" Jupyter notebook (this will take about 10 seconds)
   - The automatic setup removes the "pandas" program from the OT-2. If you need to use "pandas" on the OT-2, don't use the notebook and instead run UFACTORY’s "setup.py" program manually.
   - The setup will have an exit code of 1 (unsuccessful) if your OT-2 is not connected to the internet, but the necessary files will still be installed.
5. Reboot the OT-2

**Part 2: Network Setup**
To have the OT-2 communicate with the xArm, it needs a static IP on that Ethernet interface. You can use one of the two provided Jupyter notebooks to configure this.

First, make note of the xArm control box IP address, which is written on its side. It will be something like `192.168.1.xxx`.
* Our scripts give the OT-2 an IP address of `192.168.1.27`, which was picked arbitrarily. If the control box happens to have this same exact IP address, you will have to modify the Jupyter notebook you use to set a different IP address (e.g. `192.168.1.28`).

The Jupyter notebook to use depends on the connection between your host computer and OT-2:

*1: Computer and OT-2 are connected via Ethernet (recommended)*

Use the "ot-ufactory-wired-setup.ipynb" notebook

*2: Computer and OT-2 are connected via Wi-Fi*

Use the "ot-ufactory-wireless-setup.ipynb" notebook

* If you use the Wi-Fi configuration, you may be unable to connect your computer to the OT-2 via Ethernet. If something happens to the Wi-Fi network (e.g. the Wi-Fi password is changed), you may be locked out of your OT-2 and you will have to reflash the SD card, meaning you will lose any data you have stored on the robot: [Reflashing the OT-2's SD card](https://support.opentrons.com/s/article/Reflashing-the-OT-2-s-SD-card)

These network configurations will persist even after turning the OT-2 on/off, and/or unplugging the xArm (meaning you can safely shut down and unplug everything if you need to move equipment around). If you want to remove these network configurations, see the "Troubleshooting" section below.

### Using the xArm in an Opentrons Protocol
"protocol_ufactory.py" is an example protocol that manipulates the UFACTORY joints and Biogripper. It uses both the `set_position()` and `set_servo_angle()` functions from the xArm SDK to demonstrate how movement works. You can follow the examples in the "examples/wrapper/" folder of the SDK to build on this functionality and create movements that are useful to your workflow.

**UFACTORY Blockly Code**

In addition to manually setting the arm movements with the above functions, you can program movements in UFACTORY’s Blockly interface and convert them to Python code using the tool in "examples/wrapper/tool/". If you generate this code, you will see that it is more complicated than the examples provided by UFACTORY and the protocol here (callbacks, custom print statement). You should be able to copy and paste this code into an Opentrons protocol, but you may want to remove the code besides the core movement code to avoid possible performance and threading issues.

### Troubleshooting
If you have connection issues between the OT-2 and the xArm, you may need to SSH into the OT-2 to troubleshoot:

[Setting up SSH access to your OT-2](https://support.opentrons.com/s/article/Setting-up-SSH-access-to-your-OT-2)

[Connecting to your OT-2 with SSH](https://support.opentrons.com/s/article/Connecting-to-your-OT-2-with-SSH)

The first step is to try to ping the xArm control box from the OT-2:

`ping 192.168.1.<xxx>`

If there is no response, you can try removing the connection and manually adding it:

`nmcli con show`

Make note of the connection that has the "ufactory" name:

`nmcli con delete uuid <uuid of "ufactory" connection>`

Add connection (this is what the Jupyter notebooks are doing):

*Computer and OT-2 are connected via Ethernet*

`nmcli connection add type ethernet con-name ufactory ifname eth1 ip4 192.168.1.27/24 gw4 192.168.1.1`

*Computer and OT-2 are connected via Wi-Fi*

`nmcli connection add type ethernet con-name ufactory ifname eth0 ip4 192.168.1.27/24 gw4 192.168.1.1 connection.autoconnect-priority 2`

Reboot the OT-2.
