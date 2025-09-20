
#region ------------------------------------------------------------------------------------ Imports

import time
from fischertechnik.controller.Motor import Motor # pyright: ignore
from lib.controller import Gripper_home_switch, Gripper_motor # pyright: ignore

#endregion

#region ---------------------------------------------------------------------------------- Variables

g_max_speed = 512
g_open_timeout = 1100

g_commands = None
g_cmd_counter = None
g_current_time = None
g_state = None

#endregion

#region ---------------------------------------------------------------------------------- Functions

# Initialize variables

def Init_gripper():
    global g_commands, g_cmd_counter, g_current_time
    g_commands = []
    g_cmd_counter = 1
    g_current_time = -1


# Store command list

def Store_gripper_commands(_values):
    global g_commands
    for _item in _values:
        g_commands.append(_item)


# Start returning gripper to home position

def Reset_gripper_start():
    global g_state
    if Gripper_home_switch.is_open():
        Gripper_motor.set_speed(g_max_speed, Motor.CW)
        Gripper_motor.start()
        g_state = 'closing'


# Loop to return gripper to home position

def Reset_gripper_loop():
    global g_state
    if Gripper_home_switch.is_closed():
        Gripper_motor.stop()
        g_state = 'closed'


# Return True if gripper is at home position

def Is_gripper_reset():
    return Gripper_home_switch.is_closed() and g_state == 'closed'


# Return True if gripper is at maximum open position

# def Is_gripper_open():
#     return Gripper_home_switch.is_open() and g_state == 'open'


# Return True if timeout has expired

def Gripper_timeout(_millis):
    return (time.time() * 1000) >= g_current_time + _millis


# Command processor

def Gripper_command_loop():
    global g_cmd_counter, g_current_time
    if g_cmd_counter <= len(g_commands):
        cmd, val = g_commands[g_cmd_counter - 1]
        if cmd == 'open':
            if Move_gripper(1):
                g_cmd_counter += 1
        elif cmd == 'close':
            if Move_gripper(-1):
                g_cmd_counter += 1
        elif cmd == 'wait':
            if g_current_time < 0:
                g_current_time = time.time() * 1000
            if Gripper_timeout(val):
                g_cmd_counter += 1
                g_current_time = -1


# Move gripper to target position. Returns True when target is reached

def Move_gripper(cmd):
    global g_state, g_current_time
    if cmd > 0 and g_state == 'closed':
        if Gripper_home_switch.is_closed():
            g_state = 'opening'
            Gripper_motor.set_speed(g_max_speed, Motor.CCW)
            Gripper_motor.start()
            g_current_time = time.time() * 1000
    elif cmd < 0 and g_state == 'open':
        if Gripper_home_switch.is_open():
            g_state = 'closing'
            Gripper_motor.set_speed(g_max_speed, Motor.CW)
            Gripper_motor.start()
    else:
        if cmd < 0 and Gripper_home_switch.is_closed():
            Gripper_motor.stop()
            g_state = 'closed'
            return True
        elif cmd > 0 and Gripper_timeout(g_open_timeout):
            Gripper_motor.stop()
            g_state = 'open'
            g_current_time = -1
            return True
    return False

#endregion