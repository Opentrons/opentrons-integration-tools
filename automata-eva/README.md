# Automata Labs Eva

### Introduction
The Automata Eva can be easily controlled by the OT-2 in a protocol thanks to the Python SDK provided by Automata. There are just a few one-time setup steps to get started.

### Hardware Requirements
* Automata Eva
* Ethernet-USB adapter (optional)
* Tape (optional)

### Hardware Setup
If you connect the OT-2 and the Automata Eva via Wi-Fi, there is no additional hardware setup required besides the standard Automata setup!

If you want to connect the OT-2 and the Eva via Ethernet, you will need an Ethernet-USB adapter. Connect an Ethernet cable from the Eva to the Ethernet-USB adapter, and then plug the Ethernet-USB adapter into any of the OT-2’s USB ports.
* You may want to tape the Ethernet cable to the side or top of the OT-2 so that it doesn't go over the deck, depending on where the Eva is relative to the OT-2.

### Software Setup
**Prerequisites: Set Up SSH**

[Setting up SSH access to your OT-2](https://support.opentrons.com/s/article/Setting-up-SSH-access-to-your-OT-2)

[Connecting to your OT-2 with SSH](https://support.opentrons.com/s/article/Connecting-to-your-OT-2-with-SSH)

**Part 1: Install the Automata SDK**
1. If your OT-2 is connected to the internet, you can install the SDK with `pip install evasdk`
   - Alternatively, you can download the package from PyPI, upload it to the OT-2, and manually run the setup: https://pypi.org/project/evasdk/ 
2. Reboot the OT-2

**Part 2: Network Setup**
The Automata Eva behaves as a wireless access point by default. The first time you use it, follow the instructions from Automata on how to connect to the Eva's wireless network, set up an administrator account, and go to the configuration dashboard (called "Choreograph") from your host computer. In Choreograph, set up an API token and make note of the value.

After connecting to Choreograph and setting up an API token, you can connect the OT-2 directly to the Automata Eva in one of two ways:

*1: Wi-Fi*

To use the Opentrons app on your host computer, the computer either needs to also be connected to the Automata Eva Wi-Fi network, or connected to the OT-2 via Ethernet.

In Choreograph, make sure the "Network connection type" is set to "Access Point".

Open the Opentrons App, connect to your OT-2, and connect the OT-2 to the Automata Eva's Wi-Fi network using its credentials. That's it!

*2: Ethernet*

In Choreograph, set the "Network connection type" to "Ethernet". Set a static IP address for the Eva, e.g. `192.168.0.207`.

Give the OT-2 a static IP address with this command:

`nmcli connection add type ethernet con-name automata ifname eth1 ip4 192.168.0.27/24 gw4 192.168.0.1`

This network configuration will persist even after turning the OT-2 on/off, and/or unplugging the Eva (meaning you can safely shut down and unplug everything if you need to move equipment around). If you want to remove this network configuration, see the "Troubleshooting" section below.

### Using the Automata Eva in an Opentrons Protocol

There are two ways to control the Automata Eva in Python: loading and running an Automata toolpath, and manually controlling the joints with the `Eva.control_go_to()` function. The two example protocols show each way.

### Troubleshooting

If you have connection issues between the OT-2 and the Automata Eva, you may need to SSH into the OT-2 to troubleshoot. The first step is to try to ping the Eva from the OT-2:

`ping <Eva IP address>`

If there is no response, use the commands:

`ifconfig`

`nmcli con show`

To see information about the OT-2's network connections.

If the Eva and OT-2 are connected via Ethernet, you may need to remove the connection and create it again. Use `nmcli con show` to make note of the connection that has the "automata" name. Delete the connection with this command:

`nmcli con delete uuid <uuid of "automata" connection>`

Then add it again and reboot the OT-2:

`nmcli connection add type ethernet con-name automata ifname eth1 ip4 192.168.0.27/24 gw4 192.168.0.1`

* You can use a different IP address than `192.168.0.27`, but make sure it is on the same subnet as the Eva.

### Links
[Automata Labs Eva](https://automata.tech/products/hardware/about-eva/)

[Eva Python SDK](https://github.com/automata-tech/eva_python_sdk)
