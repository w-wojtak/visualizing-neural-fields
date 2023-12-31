import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.widgets import Slider, Button
import streamlit as st


def plot_final_state_1d(activity, field_pars):
    """
    Plots the final state of u(x,t) at time t=end.
    """
    x_lim, _, dx, _, _ = field_pars
    x = np.arange(-x_lim, x_lim + dx, dx)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, activity[-1, :])
    ax.set_xlim(-x_lim, x_lim)
    ax.set_xlabel('x')
    ax.set_ylabel('u(x)')
    return fig


def plot_animate_1d(activity, field_pars, inputs, input_flag):
    """
    Animates the time evolution of activity u(x,t) and inputs (if present).
    """
    x_lim, _, dx, _, _ = field_pars
    x = np.arange(-x_lim, x_lim + dx, dx)

    upper_lim_y = max([activity.max(), inputs.max()])
    lower_lim_y = min([activity.min(), inputs.min()])

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylim(lower_lim_y, upper_lim_y)
    ax.set_xlim(-x_lim, x_lim)
    ax.set_xlabel('x')
    ax.set_ylabel('Activity')

    if input_flag:
        line1, = ax.plot(x, activity[0, :], label='u(x)')
        line2, = ax.plot(x, inputs[0, :], label='Input')
        ax.legend()

        # Create a placeholder to display the animation
        animated_plot = st.pyplot(fig)

        for i in range(activity.shape[0]):
            if i % 10 == 0:
                line1.set_xdata(x)
                line1.set_ydata(activity[i, :])

                line2.set_xdata(x)
                line2.set_ydata(inputs[i, :])

                # Update the animated plot
                animated_plot.pyplot(fig)
                time.sleep(0.001)
    else:
        line1, = ax.plot(x, activity[0, :], label='u(x)')
        ax.legend()  # Add a legend to the plot

        # Create a placeholder to display the animation
        animated_plot = st.pyplot(fig)

        for i in range(activity.shape[0]):
            if i % 5 == 0:
                line1.set_xdata(x)
                line1.set_ydata(activity[i, :])

                # Update the animated plot
                animated_plot.pyplot(fig)
                time.sleep(0.001)


# def plot_animate_1d(activity, field_pars, inputs, input_flag):
#     """
#     Animates the time evolution of activity u(x,t) and inputs (if present).
#     """
#     x_lim, _, dx, _, _ = field_pars
#     x = np.arange(-x_lim, x_lim + dx, dx)
#
#     upper_lim_y = max([activity.max(), inputs.max()])
#     lower_lim_y = min([activity.min(), inputs.min()])
#
#     # enable interactive mode
#     plt.ion()
#     figure, ax = plt.subplots(figsize=(6, 4))
#     ax.set_ylim(lower_lim_y, upper_lim_y)
#     ax.set_xlim(-x_lim, x_lim)
#     plt.xlabel('x')
#
#     if input_flag:
#         line1, = ax.plot(x, activity[0, :], label='u(x)')
#         line2, = ax.plot(x, inputs[0, :], label='Input')
#
#         ax.legend()
#
#         for i in range(activity.shape[0]):
#             if i % 5 == 0:
#                 line1.set_xdata(x)
#                 line1.set_ydata(activity[i, :])
#
#                 line2.set_xdata(x)
#                 line2.set_ydata(inputs[i, :])
#
#                 # draw updated values
#                 figure.canvas.draw()
#                 figure.canvas.flush_events()
#                 time.sleep(0.001)
#     else:
#         line1, = ax.plot(x, activity[0, :], label='u(x)')
#
#         ax.legend()  # Add a legend to the plot
#
#         for i in range(activity.shape[0]):
#             if i % 5 == 0:
#                 line1.set_xdata(x)
#                 line1.set_ydata(activity[i, :])
#
#                 # draw updated values
#                 figure.canvas.draw()
#                 figure.canvas.flush_events()
#                 time.sleep(0.001)

# works but not needed now:
# def plot_slider_1d(activity, field_pars, inputs, input_flag):
#     """
#      Creates an interactive plot with a slider to visualize how activity and inputs change in time.
#     """
#
#     x_lim, _, dx, dt, _ = field_pars
#
#     x = np.arange(-x_lim, x_lim + dx, dx)
#
#     upper_lim_y = max([activity.max(), inputs.max()])
#     lower_lim_y = min([activity.min(), inputs.min()])
#
#     fig, ax = plt.subplots(figsize=(6, 4))
#     plt.subplots_adjust(bottom=0.25)  # Adjust the bottom margin to make space for the slider and button
#
#     line_activity, = ax.plot(x, activity[0, :], label='u(x)')
#
#     if input_flag:
#         line_input, = ax.plot(x, inputs[0, :], label='Input(x)', linestyle='dashed')
#
#     ax.legend()
#     ax.set_ylim(lower_lim_y, upper_lim_y)
#     ax.set_xlim(-x_lim, x_lim)
#     plt.xlabel('x')
#
#     ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])  # Define the slider's position [left, bottom, width, height]
#     slider = Slider(ax_slider, '', 0, activity.shape[0] - 1, valinit=0, valstep=1)
#     slider.valtext.set_visible(False)  # hide matplotlib slider values
#
#     ax_reset = plt.axes([0.8, 0.02, 0.1, 0.04])  # Define the reset button's position [left, bottom, width, height]
#     reset_button = Button(ax_reset, 'Reset')
#
#     time_label = plt.text(0.5, 0.05, f'Time Step: {slider.val * dt:.2f}', transform=fig.transFigure, ha='center')
#
#     def update(val):
#         time_step = int(slider.val)
#         line_activity.set_ydata(activity[time_step, :])
#
#         if input_flag:
#             line_input.set_ydata(inputs[time_step, :])
#
#         time_label.set_text(f'Time : {time_step * dt:.2f}')
#         fig.canvas.draw_idle()
#
#     def reset(event):
#         slider.set_val(0)
#
#     slider.on_changed(update)
#     reset_button.on_clicked(reset)
#
#     plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_space_time_flat(activity, field_pars):
    x_lim, t_lim, _, _, _ = field_pars
    x_range = [-x_lim, x_lim]
    t_range = [0.0, t_lim]

    upper_lim = activity.max()
    lower_lim = activity.min()

    fig, ax = plt.subplots(figsize=(6, 3))
    pic = ax.imshow(np.transpose(activity), cmap='plasma', vmin=lower_lim, vmax=upper_lim,
                    extent=[t_range[0], t_range[1], x_range[0], x_range[1]],
                    interpolation='nearest', origin='lower', aspect='auto')
    plt.colorbar(pic, ax=ax)
    ax.set_xlabel('t')
    ax.set_ylabel('x', rotation=0)
    ax.set_title('u(x,t)')
    plt.tight_layout()
    plt.gcf().set_dpi(300)
    return fig


def plot_space_time_3d(activity, field_pars):
    x_lim, t_lim, dx, dt, _ = field_pars
    upper_lim = activity.max()
    lower_lim = activity.min()

    x = np.arange(-x_lim, x_lim + dx, dx)
    t = np.arange(0, t_lim + dt, dt)

    x_mesh, t_mesh = np.meshgrid(x, t)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(t_mesh, x_mesh, activity, cmap=plt.get_cmap('plasma'),
                           linewidth=0, antialiased=False)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.set_box_aspect([2, 1, 1])

    fig.colorbar(surf, shrink=0.4, aspect=10, pad=0.2)

    ax.zaxis.set_rotate_label(False)

    ax.set_xlabel('t', linespacing=3.2)
    ax.set_ylabel('x', linespacing=3.1)
    ax.set_zlabel('u(x,t)', linespacing=3.4, rotation=0)

    ax.zaxis.labelpad = 10
    ax.set_zlim(lower_lim, upper_lim)

    ax.set_yticks(np.arange(-x_lim, x_lim + dx, 5))

    return fig


def plot_space_time_3d_contour(activity, field_pars):
    x_lim, t_lim, dx, dt, _ = field_pars
    z_limit = activity.max()
    contour_offset = activity.min() - 0.4

    x = np.arange(-x_lim, x_lim + dx, dx)
    t = np.arange(0, t_lim + dt, dt)

    x_mesh, t_mesh = np.meshgrid(x, t)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(t_mesh, x_mesh, activity, cmap=plt.get_cmap('plasma'),
                           linewidth=0, antialiased=False)
    ax.contourf(t_mesh, x_mesh, activity, zdir='z', offset=contour_offset, cmap='plasma')

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.set_box_aspect([2, 1, 1])

    fig.colorbar(surf, shrink=0.4, aspect=10, pad=0.2)

    ax.zaxis.set_rotate_label(False)

    ax.set_xlabel('t', linespacing=3.2)
    ax.set_ylabel('x', linespacing=3.1)
    ax.set_zlabel('u(x,t)', linespacing=3.4, rotation=0)

    ax.zaxis.labelpad = 10
    ax.set_zlim(contour_offset, z_limit)

    ax.set_yticks(np.arange(-x_lim, x_lim + dx, 5))

    return fig


def plot_time_courses(activity, field_pars, inputs, input_position):
    x_lim, t_lim, dx, dt, theta = field_pars
    x = np.arange(-x_lim, x_lim + dx, dx)
    t = np.arange(0, t_lim + dt, dt)

    figure, ax = plt.subplots(figsize=(6, 4))

    if inputs.max() > 0:
        for i in range(np.shape(input_position)[0]):
            absolute_diff = np.abs(x - input_position[i])
            bump_center = np.argmin(absolute_diff)
            ax.plot(t, activity[:, bump_center])
            ax.plot(t, inputs[:, bump_center])
    else:
        ax.plot(t, activity[:, int(len(x) / 2)])

    ax.plot(t, theta * np.ones(np.shape(t)), label='theta', linestyle='dashed')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('u(x)', rotation=0, labelpad=15)
    ax.set_xlim(t[0], t[-1])

    return figure
