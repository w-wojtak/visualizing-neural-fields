import matplotlib.pyplot as plt
from src.plotting import plot_space_time_flat, plot_final_state_1d, plot_space_time_3d, plot_space_time_3d_contour, \
    plot_animate_1d


def generate_plot(plot_type, simulation_results):
    figure = None

    if plot_type == 'Space-time (flat)':
        if 'field_activity' in simulation_results:
            figure = plot_space_time_flat(simulation_results['field_activity'], simulation_results['field_pars'])
            plt.show()
        else:
            print('Run the code to generate data before plotting.')
    elif plot_type == 'Final state':
        if 'field_activity' in simulation_results:
            figure = plot_final_state_1d(simulation_results['field_activity'], simulation_results['field_pars'])
            plt.show()
        else:
            print('Run the code to generate data before plotting.')
    elif plot_type == 'Space-time (3d)':
        if 'field_activity' in simulation_results:
            figure = plot_space_time_3d(simulation_results['field_activity'], simulation_results['field_pars'])
            plt.show()
        else:
            print('Run the code to generate data before plotting.')
    elif plot_type == 'Space-time (3d) + contour':
        if 'field_activity' in simulation_results:
            figure = plot_space_time_3d_contour(simulation_results['field_activity'], simulation_results['field_pars'])
            plt.show()
        else:
            print('Run the code to generate data before plotting.')
    elif plot_type == 'Animated':
        if 'field_activity' in simulation_results:
            figure = plot_animate_1d(simulation_results['field_activity'], simulation_results['field_pars'],
                                     simulation_results['inputs'], simulation_results['input_flag'])
            plt.show()
        else:
            print('Run the code to generate data before plotting.')

    return figure
