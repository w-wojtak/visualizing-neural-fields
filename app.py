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
col1, col2 = st.columns([1, 1])

# Column 1: Text area for user input
with col1:
    kernel_type = st.selectbox('Choose kernel type:',
                             ['Gaussian', 'Mex-hat'],
                             key='kernel_type')

    # Create text area for user input based on kernel type
    if kernel_type == 'Gaussian':
        kernel_pars = st.text_area("Enter Gaussian kernel parameters:", value=default_kernel_pars_gauss, height=20)
        exec(kernel_pars, globals())
    elif kernel_type == 'Mex-hat':
        kernel_pars = st.text_area("Enter Mex-hat kernel parameters:", value=default_kernel_pars_mex, height=20)
        exec(kernel_pars, globals())

    # if kernel_type:
    #     exec(kernel_pars, globals())

    code_snippet = st.text_area("Enter your model parameters here:", value=default_code, height=300)
    run_button = st.button('Run')
    simulate_message = st.empty()  # Placeholder for simulate_amari message
    if run_button:
        # Check if the user provided code, then evaluate and populate DataFrame
        if code_snippet:
            try:
                exec(code_snippet, globals())
                if 'field_activity' in globals():
                    if all(v is not None for v in [input_shape, input_position, input_onset_time, input_duration]):
                        input_pars = [input_shape, input_position, input_onset_time, input_duration]
                        field_activity, inputs = simulate_amari(kernel_type, field_pars, kernel_pars, input_flag, input_pars,
                                                                initial_condition_shape)
                        st.session_state.simulation_results['field_activity'] = field_activity
                        st.session_state.simulation_results['inputs'] = inputs
                        st.session_state.simulation_results['field_pars'] = field_pars
                        st.session_state.simulation_results['input_flag'] = input_flag
                        simulate_message.success('simulate_amari function executed successfully!')

            except Exception as e:
                st.write('An error occurred:', e)

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
