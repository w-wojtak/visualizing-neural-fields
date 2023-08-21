import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from src.default_values import *
from src.utils import *
from src.plotting import *
from src.helpers import generate_plot
import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)

# Set page configuration to wider layout
st.set_page_config(layout="wide")

# Initialize session state to store simulation results
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = {}

# Variables to store the simulation results
field_activity = None
inputs = None
input_shape = None
input_position = None
input_onset_time = None
input_duration = None
input_pars = [input_shape, input_position, input_onset_time, input_duration]

# Create two columns
col1, col2 = st.columns([1.05, 0.95])

# Column 1: Text area for user input
with col1:
    col3, col4 = st.columns([0.3, 0.7])
    with col3:
        kernel_type = st.selectbox('Kernel type:',
                                   ['Gaussian', 'Mex-hat', 'Oscillatory'],
                                   key='kernel_type')
    with col4:
        # Create text area for user input based on kernel type
        if kernel_type == 'Gaussian':
            kernel_parameters = st.text_area("Gaussian kernel parameters and threshold for the activation function:",
                                       value=default_kernel_pars_gauss.strip(),
                                       height=20)
            exec(kernel_parameters, globals())
        elif kernel_type == 'Mex-hat':
            kernel_parameters = st.text_area("Mex-hat kernel parameters and threshold for the activation function:",
                                       value=default_kernel_pars_mex.strip(),
                                       height=20)
            exec(kernel_parameters, globals())
        elif kernel_type == 'Oscillatory':
            kernel_parameters = st.text_area("Oscillatory kernel parameters and threshold for the activation function:",
                                       value=default_kernel_pars_osc.strip(),
                                       height=20)
            exec(kernel_parameters, globals())

    with col3:
        simulation_type = st.selectbox('Input / no input:',
                                       ['Input', 'No input'],
                                       key='simulation_type')

        if simulation_type == 'Input':
            input_flag = True
        elif simulation_type == 'No input':
            input_flag = False

        # Space is set as [-x_lim, x_lim], time as [0, t_lim]
        # st.write("Field parameters")
        code_limits = st.text_area(" Limits for space and time:", value=default_limits.strip(),
                                  height=20)
        exec(code_limits, globals())
        code_dicsr = st.text_area("Spatial and temporal discretization:",
                                   value=default_discr.strip(),
                                   height=20)
        exec(code_dicsr, globals())

    with col4:
        if simulation_type == 'Input':
            code_input = st.text_area("Input shape (amplitude, sigma) and position:", value=default_input.strip(), height=20)
            exec(code_input, globals())
            code_input_time = st.text_area("Input timing (onset time and duration):", value=default_input_time.strip(), height=20)
            exec(code_input_time, globals())
            initial_condition_shape = None
            st.write("Note: input_position, input_onset_time and input_duration must have the same length.")
        elif simulation_type == 'No input':
            code_ic = st.text_area("Initial condition parameters: (position, amplitude, sigma)", value=default_ic.strip(), height=20)
            exec(code_ic, globals())

    run_button = st.button('Run simulation')
    simulate_message = st.empty()  # Placeholder for simulate_amari message
    if run_button:
        field_pars = [x_lim, t_lim, dx, dt, theta]
        if 'field_activity' in globals():
            if all(v is not None for v in [input_shape, input_position, input_onset_time, input_duration]):
                input_pars = [input_shape, input_position, input_onset_time, input_duration]
                field_activity, inputs = simulate_amari(kernel_type, field_pars, kernel_parameters, input_flag,
                                                        input_pars,
                                                        initial_condition_shape)
                st.session_state.simulation_results['field_activity'] = field_activity
                st.session_state.simulation_results['inputs'] = inputs
                st.session_state.simulation_results['field_pars'] = field_pars
                st.session_state.simulation_results['input_flag'] = input_flag
                simulate_message.success('simulate_amari function executed successfully!')


# Column 2: Choose plot type and buttons
with col2:
    # Choose plot type before generating the plot
    plot_type = st.selectbox('Choose plot type:',
                             ['Final state', 'Space-time (flat)', 'Space-time (3d)', 'Space-time (3d) + contour'],
                             key='plot_type')

    # Create buttons using provided code snippet
    button_text = ['Plot']  # Removed 'Download figure' from button text
    if button_text[0] == 'Plot':
        figure = generate_plot(plot_type, st.session_state.simulation_results)  # Generate the figure
        if figure is not None:
            st.pyplot(figure)  # Display the figure

            # Save the figure to a bytes-like object
            img_stream = BytesIO()
            figure.savefig(img_stream, format="png")
            img_stream.seek(0)  # Move back to the beginning of the stream

            # Get the current date and create the filename
            current_datetime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
            file_name = f"{plot_type}_{current_datetime}.png"

            # Display the download button
            st.download_button(
                label="Download figure",
                data=img_stream,
                file_name=file_name,
                mime="image/png"
            )

        else:
            st.write('Figure generation failed. Make sure to run the simulation first.')
