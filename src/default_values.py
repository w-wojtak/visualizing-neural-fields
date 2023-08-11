default_code = """
# Kernel parameters
kernel_type: 1  # 0: Gaussian, 1: Mex-hat, 2: Oscillatory.

# Parameters of the mex-hat kernel: a_ex, s_ex, a_in, s_in, w_in.
kernel_pars = [1, 0.3, 0.4, 0.5, 0.05]

# Field parameters
x_lim, t_lim = 6, 20  # Limits for space and time. Space is set as [-x_lim, x_lim], time as [0, t_lim].
dx, dt = 0.01, 0.01  # Spatial and temporal discretization.
theta = 0.1  # Threshold for the activation function.
field_pars = [x_lim, t_lim, dx, dt, theta]

# Input parameters
input_flag = True  # Flag indicating if inputs are present.
input_shape = [0.7, 0.3]  # parameters of gaussian inputs: amplitude, sigma.
input_position = [-2, 2]  # input_position, input_onset_time and input_duration must have the same length.
input_onset_time = [2, 5]
input_duration = [1, 1]

# Initial condition - gaussian (if input_flag = False).
initial_condition_shape = [0, 0.5, 0.2]  # position, amplitude, sigma
"""