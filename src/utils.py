import numpy as np
import streamlit as st


def kernel_mex(x, a_ex, s_ex, a_in, s_in, w_in):
    return a_ex * np.exp(-0.5 * x ** 2 / s_ex ** 2) - a_in * np.exp(-0.5 * x ** 2 / s_in ** 2) - w_in


def kernel_gauss(x, a_ex, s_ex, w_in):
    return a_ex * np.exp(-0.5 * x ** 2 / s_ex ** 2) - w_in


def kernel_osc(x, a, b, alpha):
    return a * (np.exp(-b * abs(x)) * ((b * np.sin(abs(alpha * x))) + np.cos(alpha * x)))


def simulate_amari(kernel_type, field_pars, kernel_pars, input_flag, input_pars, initial_condition_shape):
    x_lim, t_lim, dx, dt, theta = field_pars

    x = np.arange(-x_lim, x_lim + dx, dx)
    t = np.arange(0, t_lim + dt, dt)

    history_u = np.zeros([len(t), len(x)])

    inputs = get_inputs(x, t, dt, input_pars, input_flag)
    u_0 = get_initial_condition(x, initial_condition_shape, input_flag)
    u_field = u_0

    # kernel and its fft
    if kernel_type == 'Gaussian':
        w_hat = np.fft.fft(kernel_gauss(x, *kernel_pars))
    elif kernel_type == 'Mex-hat':
        w_hat = np.fft.fft(kernel_mex(x, *kernel_pars))
    elif kernel_type == 'Oscillatory':
        w_hat = np.fft.fft(kernel_osc(x, *kernel_pars))

    for i in range(0, len(t)):
        f_hat = np.fft.fft(np.heaviside(u_field - theta, 1))
        conv = dx * np.fft.ifftshift(np.real(np.fft.ifft(f_hat * w_hat)))
        u_field = u_field + dt * (-u_field + conv + inputs[i, :])
        history_u[i, :] = u_field

    return history_u, inputs


def get_inputs(x, t, dt, input_pars, input_flag):
    input_shape, input_position, input_onset_time, input_duration = input_pars
    inputs = np.zeros([len(t), len(x)])

    if input_flag:
        # Check if the lengths of the three lists are equal
        if len(input_position) == len(input_onset_time) == len(input_duration):

            for i in range(np.shape(input_onset_time)[0]):
                # create a gaussian pattern for the current input
                input_pattern = input_shape[0] * np.exp(-0.5 * (x - input_position[i]) ** 2 / input_shape[1] ** 2)
                input_onset = int(input_onset_time[i] / dt)
                inputs[input_onset:input_onset + int(input_duration[i] / dt), :] = input_pattern

        else:
            st.warning("Warning: The lists with input parameters (input_position, input_onset_time, input_duration) "
                       "must have the same length.")

    return inputs


def get_initial_condition(x, ic_shape, input_flag):
    if input_flag:
        u_0 = np.zeros(np.shape(x))
    else:
        u_0 = ic_shape[1] * np.exp(-0.5 * (x - ic_shape[0]) ** 2 / ic_shape[2] ** 2)

    return u_0
