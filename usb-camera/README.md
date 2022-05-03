# Integrating a USB Camera

### Introduction
The OT-2 has a built-in camera that can be used to take pictures and videos of the deck. However, there may be cases where a different camera angle or position is needed, making an external camera necessary.

### Integration Summary
If your camera is compatible with Linux, you can plug it in to the Raspberry Pi via USB and it will be found by Linux’s Video4Linux utility. A device file for it will appear in `/dev/`, e.g. `/dev/video2`. Use the camera's USB ID found in `/dev/v4l/by-id` to programmatically ensure that you are using the correct camera. `find_external_camera.py` is a simple Python module that does this.

Knowing which device file is the one for your camera, you can use the `ffmpeg` tool to take pictures and videos following the instructions in [this article](https://support.opentrons.com/s/article/Using-the-OT-2-s-camera).

`protocol_external_camera.py` is an example of how you can write a protocol that uses an external camera (there are multiple ways to do it, but in this case, it may be easiest to just include everything in one Python file).

### List of Cameras that are Known to be Compatible
* [Logitech C270](https://www.logitech.com/en-us/products/webcams/c270-hd-webcam.960-000694.html)
* [Sandberg USB Office Webcam 1080p HD](https://sandberg.world/en-gb/support/usb-office-webcam-1080p-hd)
