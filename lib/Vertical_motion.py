
# region ----------------------------------------------------------------------------------- Imports

import time
from fischertechnik.controller.Motor import Motor  # pyright: ignore
from lib.controller import Vertical_home_switch, Vertical_encodermotor  # pyright: ignore

# endregion

# region --------------------------------------------------------------------------------- Variables

v_max_speed = 512
v_max_range = 480

v_commands = None
v_counter = None
v_current_time = None
v_offset = None
v_state = None

# endregion

# region --------------------------------------------------------------------------------- Functions

# Initialize variables

def Init_vertical():
    global v_commands, v_counter, v_current_time, v_offset, v_state
    v_commands = []
    v_counter = 1
    v_current_time = -1
    v_offset = 0
    v_state = 'stopped'


# Store command list

def Store_vertical_commands(_values):
    global v_commands
    for _item in _values:
        v_commands.append(_item)


# Start returning to home position

def Reset_vertical_start():
    global v_state
    if Vertical_home_switch.is_open():
        Vertical_encodermotor.set_speed(v_max_speed, Motor.CW)
        Vertical_encodermotor.start()
        v_state = 'going down'

# Loop to return to home position

def Reset_vertical_loop():
    global v_state, v_offset
    if Vertical_home_switch.is_closed():
        Vertical_encodermotor.stop()
        v_state = 'stopped'
        v_offset = 0


# Return True if motor is at home position

def Is_vertical_reset():
    return Vertical_home_switch.is_closed() and v_state == 'stopped' and v_offset == 0


# Return True if timeout has expired

def Vertical_timeout(_millis):
    return (time.time() * 1000) >= v_current_time + _millis


# Command processor

def Vertical_command_loop():
    global v_counter, v_current_time
    if v_counter <= len(v_commands):
        cmd, val = v_commands[v_counter - 1]
        if cmd == 'move':
            if Move_vertically(val):
                v_counter += 1
        elif cmd == 'wait':
            if v_current_time < 0:
                v_current_time = time.time() * 1000
            if Vertical_timeout(val):
                v_counter += 1
                v_current_time = -1


# Move to target position

def Move_vertically(_target):
    global v_offset, v_state
    if v_state == 'stopped' and 0 <= _target <= v_max_range:
        if _target > v_offset:
            v_state = 'going up'
            Vertical_encodermotor.set_speed(v_max_speed, Motor.CCW)
            Vertical_encodermotor.set_distance(_target - v_offset)
        elif _target < v_offset:
            v_state = 'going down'
            Vertical_encodermotor.set_speed(v_max_speed, Motor.CW)
            Vertical_encodermotor.set_distance(v_offset - _target)
    else:
        if v_state != 'stopped' and not Vertical_encodermotor.is_running():
            Vertical_encodermotor.stop()
            v_state = 'stopped'
            v_offset = _target
            return True
    return False

# endregion
