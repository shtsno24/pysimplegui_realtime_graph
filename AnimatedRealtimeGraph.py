"""
https://qiita.com/bear_montblanc/items/cce4e8c58dfa236200f6
https://pysimplegui.readthedocs.io/en/latest/cookbook/#animated-matplotlib-graph

"""

import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotter


def draw_figure(canvas, figure):
    # Draw Canvas
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def make_dpi_aware():
    # Avoid GUI blurring.
    import ctypes
    import platform
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)


if __name__ == "__main__":

    try:
        make_dpi_aware()

        # Generate Layout
        layout = [[sg.Text('Fast_Render_Matplotlib Plot')],
                  [sg.Canvas(key='-CANVAS-')],
                  [sg.Button("Add"), sg.Button("Clear")]]

        # Generate Window (finalize=True is Required)
        window = sg.Window('Embedding Fast_Render_Matplotlib In PySimpleGUI',
                           layout,
                           finalize=True,
                           element_justification='center',
                           font='Monospace 18')

        # Generate Fig to Embedding Graph
        fig = plt.figure(figsize=(5, 4))
        line_ax = fig.add_subplot(2, 1, 1)
        pos_ax = fig.add_subplot(2, 1, 2)
        points_num = 500
        scatter_view = plotter.Scatter(fig, pos_ax, len_points=points_num, show_icon=True, PySimpleGUI=True)
        line_view = plotter.Line(fig, line_ax, plot_area=(points_num, 1000), len_points=points_num, PySimpleGUI=True)

        # Associate Fig and Canvas.
        fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        while True:
            event, values = window.read()

            if event in (None, "Cancel"):
                break
            elif event == "Add":
                # Generate Random Data
                rand_array_x = np.random.randint(-1000, 1000, 1250).tolist()
                rand_array_y = np.random.randint(-1000, 1000, 1250).tolist()
                y = np.random.randint(-1000, 1000, points_num)

                # Plot Data
                line_view.plot(y)
                scatter_view.plot([rand_array_x, rand_array_y])

            elif event == "Clear":
                line_view.cla()
                scatter_view.cla()
                fig_agg.draw()

    except Exception as e:
        print(e, end="\n\n")
        import traceback
        traceback.print_exc()
        input("Press any key to continue...")
    else:
        print("Done")
    finally:
        window.close()
