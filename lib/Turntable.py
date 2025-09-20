
# region ----------------------------------------------------------------------------------- Imports

import time
from fischertechnik.controller.Motor import Motor  # pyright: ignore
from lib.controller import Turntable_home_switch, Turntable_encodermotor  # pyright: ignore

# endregion

# region --------------------------------------------------------------------------------- Variables

t_max_speed = 512
t_min_range = -200
t_max_range = 800

t_commands = None
t_counter = None
t_current_time = None
t_offset = None
t_state = None

# endregion

# region --------------------------------------------------------------------------------- Functions

# Initialize variables

def Init_turntable():
    global t_commands, t_counter, t_current_time, t_offset, t_state
    t_commands = []
    t_counter = 1
    t_current_time = -1
    t_offset = 0
    t_state = 'stopped'


# Store command list

def Store_turntable_commands(_values):
    global t_commands
    for _item in _values:
        t_commands.append(_item)


# Start returning to home position

def Reset_turntable_start():
    global t_state
    if Turntable_home_switch.is_open():
        Turntable_encodermotor.set_speed(t_max_speed, Motor.CW)
        Turntable_encodermotor.start()
        t_state = 'going down'


# Loop to return to home position

def Reset_turntable_loop():
    global t_state, t_offset
    if Turntable_home_switch.is_closed():
        Turntable_encodermotor.stop()
        t_state = 'stopped'
        t_offset = 0


# Return True if motor is at home position

def Is_turntable_reset():
    return Turntable_home_switch.is_closed() and t_state == 'stopped' and t_offset == 0


# Return True if timeout has expired

def Turntable_timeout(_millis):
    return (time.time() * 1000) >= t_current_time + _millis


# Command processor

def Turntable_command_loop():
    global t_counter, t_current_time
    if t_counter <= len(t_commands):
        cmd, val = t_commands[t_counter - 1]
        if cmd == 'move':
            if Move_turntablely(val):
                t_counter += 1
        elif cmd == 'wait':
            if t_current_time < 0:
                t_current_time = time.time() * 1000
            if Turntable_timeout(val):
                t_counter += 1
                t_current_time = -1


# Move to target position

def Move_turntablely(_target):
    global t_offset, t_state
    if t_state == 'stopped' and t_min_range <= _target <= t_max_range:
        if _target > t_offset:
            t_state = 'going up'
            Turntable_encodermotor.set_speed(t_max_speed, Motor.CCW)
            Turntable_encodermotor.set_distance(_target - t_offset)
        elif _target < t_offset:
            t_state = 'going down'
            Turntable_encodermotor.set_speed(t_max_speed, Motor.CW)
            Turntable_encodermotor.set_distance(t_offset - _target)
    else:
        if t_state != 'stopped' and not Turntable_encodermotor.is_running():
            Turntable_encodermotor.stop()
            t_state = 'stopped'
            t_offset = _target
            return True
    return False

# endregion
