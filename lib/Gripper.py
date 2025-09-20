import time
from fischertechnik.controller.Motor import Motor # pyright: ignore
from lib.controller import *

M4_delay = None
M4_state = None


def Init_gripper():
    global M4_delay, M4_state
    M4_delay = 700


def Close_gripper_sync():
    global M4_delay, M4_state
    Reset_gripper_start()
    while Gripper_mini_switch.is_open():
        time.sleep(0.01)
    Gripper_motor.stop()
    M4_state = 'closed'


def Test_gripper_sync():
    global M4_delay, M4_state
    Open_gripper_sync()
    time.sleep(1)
    Close_gripper_sync()


def Reset_gripper_start():
    global M4_delay, M4_state
    if Gripper_mini_switch.is_open():
        Gripper_motor.set_speed(int(512), Motor.CW)
        Gripper_motor.start()
        M4_state = 'closing'


def Open_gripper_sync():
    global M4_delay, M4_state
    if Gripper_mini_switch.is_closed():
        Gripper_motor.set_speed(int(512), Motor.CCW)
        Gripper_motor.start()
        M4_state = 'opening'
        time.sleep(M4_delay / 1000)
        Gripper_motor.stop()
        M4_state = 'opened'


def Reset_gripper_loop():
    global M4_delay, M4_state
    if Gripper_mini_switch.is_closed():
        Gripper_motor.stop()
        M4_state = 'closed'
