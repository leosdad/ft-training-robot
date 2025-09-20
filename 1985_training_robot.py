
#region ------------------------------------------------------------------------------------ Imports

from lib.controller import *
from lib.Turntable import *
from lib.Vertical_motion import *
from lib.Horizontal_motion import *
from lib.Gripper import *

#endregion

#region ---------------------------------------------------------------------------------- Functions

def Turntable_commands():
    return [
        ['wait', 400],  # Wait for gripper to close
        ['move', -100],
        ['wait', 400],
        ['move', 100],
        ['wait', 400],
        ['move', 0],
    ]


def Vertical_commands():
    return [
        ['wait', 400],  # Wait for gripper to close
        # ['wait', 1000],
        ['move', 100],
        # ['wait', 400],
        # ['move', 350],
        ['wait', 600],
        ['move', 0],
    ]


def Horizontal_commands():
    return [
        ['wait', 400],  # Wait for gripper to close
        ['move', 200],
        # ['wait', 100],
        # ['move', 280],
        ['wait', 300],
        # ['move', 110],
        # ['wait', 100],
        ['move', 0],
    ]

def Gripper_commands():
    return [
        # ['open', 0],
        # ['wait', 500],
        ['close', 0],
        ['wait', 4500],
        ['open', 0],
    ]

#endregion

#region ------------------------------------------------------------------------------- Main program

# Initialize all

Init_turntable()
Init_vertical()
Init_horizontal()
Init_gripper()

# Reset all

Reset_turntable_start()
Reset_vertical_start()
Reset_horizontal_start()
Reset_gripper_start()

while not (Is_turntable_reset()):
    Reset_turntable_loop()
while not (Is_vertical_reset()):
    Reset_vertical_loop()
while not (Is_horizontal_reset()):
    Reset_horizontal_loop()
while not (Is_gripper_reset()):
    Reset_gripper_loop()

# Store commands

Store_turntable_commands(Turntable_commands())
Store_vertical_commands(Vertical_commands())
Store_horizontal_commands(Horizontal_commands())
Store_gripper_commands(Gripper_commands())

# Main loop

while True:
    Turntable_command_loop()
    Vertical_command_loop()
    Horizontal_command_loop()
    Gripper_command_loop()

#endregion -----------------------------------------------------------------------------------------
