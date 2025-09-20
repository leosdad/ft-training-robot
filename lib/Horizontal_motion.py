
# region ----------------------------------------------------------------------------------- Imports

import time
from fischertechnik.controller.Motor import Motor  # pyright: ignore
from lib.controller import Horizontal_home_switch, Horizontal_encodermotor  # pyright: ignore

# endregion

# region --------------------------------------------------------------------------------- Variables

h_max_speed = 512
h_max_range = 330

h_commands = None
h_counter = None
h_current_time = None
h_offset = None
h_state = None

# endregion

# region --------------------------------------------------------------------------------- Functions

# Initialize variables

def Init_horizontal():
    global h_commands, h_counter, h_current_time, h_offset, h_state
    h_commands = []
    h_counter = 1
    h_current_time = -1
    h_offset = 0
    h_state = 'stopped'


# Store command list

def Store_horizontal_commands(_values):
    global h_commands
    for _item in _values:
        h_commands.append(_item)


# Start returning to home position

def Reset_horizontal_start():
    global h_state
    if Horizontal_home_switch.is_open():
        Horizontal_encodermotor.set_speed(h_max_speed, Motor.CW)
        Horizontal_encodermotor.start()
        h_state = 'going backward'


# Loop to return to home position

def Reset_horizontal_loop():
    global h_state, h_offset
    if Horizontal_home_switch.is_closed():
        Horizontal_encodermotor.stop()
        h_state = 'stopped'
        h_offset = 0


# Return True if motor is at home position

def Is_horizontal_reset():
    return Horizontal_home_switch.is_closed() and h_state == 'stopped' and h_offset == 0


# Return True if timeout has expired

def Horizontal_timeout(_millis):
    return (time.time() * 1000) >= h_current_time + _millis


# Command processor

def Horizontal_command_loop():
    global h_counter, h_current_time
    if h_counter <= len(h_commands):
        cmd, val = h_commands[h_counter - 1]
        if cmd == 'move':
            if Move_horizontally(val):
                h_counter += 1
        elif cmd == 'wait':
            if h_current_time < 0:
                h_current_time = time.time() * 1000
            if Horizontal_timeout(val):
                h_counter += 1
                h_current_time = -1


# Move to target position

def Move_horizontally(_target):
    global h_offset, h_state
    if h_state == 'stopped' and 0 <= _target <= h_max_range:
        if _target > h_offset:
            h_state = 'going forward'
            Horizontal_encodermotor.set_speed(h_max_speed, Motor.CCW)
            Horizontal_encodermotor.set_distance(_target - h_offset)
        elif _target < h_offset:
            h_state = 'going backward'
            Horizontal_encodermotor.set_speed(h_max_speed, Motor.CW)
            Horizontal_encodermotor.set_distance(h_offset - _target)
    else:
        if h_state != 'stopped' and not Horizontal_encodermotor.is_running():
            Horizontal_encodermotor.stop()
            h_state = 'stopped'
            h_offset = _target
            return True
    return False

# endregion
