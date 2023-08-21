default_code = """
x_lim, t_lim = 10, 15  # Limits for space and time. Space is set as [-x_lim, x_lim], time as [0, t_lim].
dx, dt = 0.0025, 0.01  # Spatial and temporal discretization.
theta = 0.1  # Threshold for the activation function.
field_pars = [x_lim, t_lim, dx, dt, theta]
"""

default_ic = """
initial_condition_shape = [0, 0.5, 0.2] 
"""

default_input = """
input_shape = [2.5, 0.5] 
input_position = [-2]
"""

default_input_time = """
input_onset_time = [2]
input_duration = [1]
"""

default_kernel_pars_mex = """ 
kernel_parameters = [1.3, 0.4, 0.5, 0.5, 0.15]
"""

default_kernel_pars_gauss = """
kernel_parameters = [1, 0.4, 0.2]
"""

default_kernel_pars_osc = """
kernel_parameters = [1, 0.3, 0.9]
"""