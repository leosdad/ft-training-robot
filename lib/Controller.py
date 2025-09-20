
#region ------------------------------------------------------------------------------------ Imports

import fischertechnik.factories as txt_factory # type: ignore

#endregion

#region ----------------------------------------------------------------------------- Initialization

txt_factory.init()
txt_factory.init_input_factory()
txt_factory.init_motor_factory()

#endregion

#region ----------------------------------------------------------- Controller, inputs and actuators

TXT_M = txt_factory.controller_factory.create_graphical_controller()

# Turntable
Turntable_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 1)
Turntable_home_switch = txt_factory.input_factory.create_mini_switch(TXT_M, 1)
Turntable_left_switch = txt_factory.input_factory.create_mini_switch(TXT_M, 5)

# Vertical motion
Vertical_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 2)
Vertical_home_switch = txt_factory.input_factory.create_mini_switch(TXT_M, 2)

# Horizontal motion
Horizontal_encodermotor = txt_factory.motor_factory.create_encodermotor(TXT_M, 3)
Horizontal_home_switch = txt_factory.input_factory.create_mini_switch(TXT_M, 3)

# Gripper
Gripper_motor = txt_factory.motor_factory.create_motor(TXT_M, 4)
Gripper_mini_switch = txt_factory.input_factory.create_mini_switch(TXT_M, 4)

#endregion

txt_factory.initialized()
