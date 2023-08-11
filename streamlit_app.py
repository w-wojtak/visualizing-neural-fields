import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.default_values import default_code
from src.utils import *
from src.plotting import *

# Set page configuration to wider layout
st.set_page_config(layout="wide")

# Initialize session state to store data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

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
col1, col2 = st.columns(2)

# Column 1: Text area for user input
with col1:
    code_snippet = st.text_area("Enter your model parameters here:", value=default_code, height=300)
    run_button = st.button('Run')
    simulate_message = st.empty()  # Placeholder for simulate_amari message
    if run_button:
        # Check if the user provided code, then evaluate and populate DataFrame
        if code_snippet:
            try:
                exec(code_snippet, globals())
                if 'data' in globals():
                    st.session_state.data = data  # Store 'x' and 'y' data in session state
                if 'field_activity' in globals():
                    if all(v is not None for v in [input_shape, input_position, input_onset_time, input_duration]):
                        input_pars = [input_shape, input_position, input_onset_time, input_duration]
                        field_activity, inputs = simulate_amari(field_pars, kernel_pars, input_flag, input_pars,
                                                                initial_condition_shape)
                        st.session_state.simulation_results['field_activity'] = field_activity
                        st.session_state.simulation_results['inputs'] = inputs
                        st.session_state.simulation_results['field_pars'] = field_pars
                        st.session_state.simulation_results['input_flag'] = input_flag
                        simulate_message.success('simulate_amari function executed successfully!')

            except Exception as e:
                st.write('An error occurred:', e)

# Column 2: Choose plot type and Plot button
with col2:
    # Choose plot type before generating the plot
    plot_type = st.selectbox('Choose plot type:', ['Final state', 'Space-time (flat)', 'Space-time (3d)', 'Space-time (3d) + contour', 'Slider', 'Animated'], key='plot_type')

    # Plot button to generate the selected plot type
    plot_button = st.button('Plot', key='plot_button')
    if plot_button:
        # if plot_type == 'Line Chart':
        #     if not st.session_state.data.empty:
        #         plt.plot(st.session_state.data['x'], st.session_state.data['y'])
        #         st.pyplot(plt)
        #     else:
        #         st.write('Run the code to generate data before plotting.')
        if plot_type == 'Space-time (flat)':
            if 'field_activity' in st.session_state.simulation_results:
                plot_space_time_flat(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
        elif plot_type == 'Final state':
            if 'field_activity' in st.session_state.simulation_results:
                plot_final_state_1d(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
        elif plot_type == 'Space-time (3d)':
            if 'field_activity' in st.session_state.simulation_results:
                plot_space_time_3d(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
        elif plot_type == 'Space-time (3d) + contour':
            if 'field_activity' in st.session_state.simulation_results:
                plot_space_time_3d_contour(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
        elif plot_type == 'Slider':
            if 'field_activity' in st.session_state.simulation_results:
                plot_slider_1d(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'], st.session_state.simulation_results['inputs'], st.session_state.simulation_results['input_flag'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
        elif plot_type == 'Animated':
            if 'field_activity' in st.session_state.simulation_results:
                plot_animate_1d(st.session_state.simulation_results['field_activity'], st.session_state.simulation_results['field_pars'], st.session_state.simulation_results['inputs'], st.session_state.simulation_results['input_flag'])
                st.pyplot(plt)
            else:
                st.write('Run the code to generate data before plotting.')
