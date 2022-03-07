import sys

from opentrons import protocol_api

sys.path.append("/var/lib/jupyter/notebooks/xArm-Python-SDK-master")
from xarm.wrapper import XArmAPI

# Set your IP address here
UFACTORY_IP = "192.168.1.207"


metadata = {
    'protocolName': 'UFACTORY Example',
    'author': 'Nicolas Binford <nicolas.binford@opentrons.com>',
    'description': 'Move the UFACTORY arm in a protocol',
    'apiLevel': '2.12'
}


def ufactory_action(ctx):

    ctx.comment("UFACTORY action function")

    # Instantiate arm
    arm = XArmAPI(UFACTORY_IP)
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    # Enable biogripper
    arm.set_bio_gripper_enable(True)
    arm.set_bio_gripper_speed(300)

    arm.reset(wait=True)

    # Box/starting position
    arm.set_position(x=200, y=0, z=110, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Start gripper as open
    arm.open_bio_gripper()
    ctx.delay(seconds=1)

    # Move base joint
    arm.set_servo_angle(servo_id=1, angle=45, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Grab object
    code = arm.close_bio_gripper()
    ctx.delay(seconds=1)

    # Move second joint up
    arm.set_servo_angle(servo_id=2, angle=-10, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Move base joint back over
    arm.set_servo_angle(servo_id=1, angle=0, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Move second joint back down
    arm.set_servo_angle(servo_id=2, angle=0, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Drop object
    arm.open_bio_gripper()
    ctx.delay(seconds=1)

    # Back to starting position
    arm.set_position(x=200, y=0, z=110, speed=50, wait=True)
    ctx.delay(seconds=1)

    # Cleanup
    arm.reset(wait=True)
    arm.disconnect()


def run(ctx):

    # Load labware and pipette
    tip_rack = ctx.load_labware("opentrons_96_tiprack_300ul", 9)
    p300 = ctx.load_instrument("p300_single", "right",
                               tip_racks=[tip_rack])

    # Opentrons action
    p300.move_to(tip_rack['A1'].top())

    # UFACTORY action
    if not ctx.is_simulating():
        ufactory_action(ctx)

    # Opentrons action
    p300.pick_up_tip()
    p300.drop_tip()
