import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from typing import List

from ffi import FFI
from statistics import Statistics


class OperationComboBox(ttk.Combobox):
    def __init__(self, parent, operations, *args, **kwargs):
        operation_names = [op.name for op in operations.values()]
        super().__init__(
            parent,
            values=operation_names,
            state='readonly',
            *args,
            **kwargs
        )


class GraphTypeComboBox(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            values=[
                'Scatter',
                'Line',
                'Bar',
                'Histogram',
                'Boxplot',
                'Rolling Average',
            ],
            state='readonly',
            *args,
            **kwargs
        )


class MetricTypeListbox(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            selectmode=tk.MULTIPLE,
            exportselection=False,
            *args,
            **kwargs
        )

        for metric in Statistics.statistics_map:
            self.insert(tk.END, metric)

    def get_selected_metrics(self):
        return [self.get(i) for i in self.curselection()]


class GraphCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrollbar = ttk.Scrollbar(
            parent,
            orient=tk.VERTICAL,
            command=self.yview
        )
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.bind('<Configure>', self.on_configure)

        self.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_configure(self, event):
        self.configure(scrollregion=self.bbox('all'))

    def add_graph_frame(self):
        graph_frame = tk.Frame(self.scrollable_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        return graph_frame

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.yview_scroll(1, 'units')
        elif event.num == 4 or event.delta == 120:
            self.yview_scroll(-1, 'units')


class IterationsEntryBox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = ttk.Label(self, text='Iterations:')
        self.label.pack(pady=5)

        self.iterations_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.iterations_var)
        self.entry.pack(pady=5)

    def get_iterations(self):
        try:
            return int(self.iterations_var.get())
        except ValueError:
            return 1


class Graphs:
    def line(ax, indices, values, label, color):
        ax.plot(indices, values, label=label, color=color)

    def bar(ax, indices, values, label, color):
        ax.bar(indices, values, label=label, color=color)

    def scatter(ax, indices, values, label, color):
        ax.scatter(indices, values, label=label, color=color, s=10, alpha=0.5)

    def histogram(ax, indices, values, label, color):
        ax.hist(values, label=label, bins=20, color=color, alpha=0.7)
        ax.set_ylabel('Frequency')

    def boxplot(ax, indices, values, label, color):
        ax.boxplot(
            values,
            label=label,
            vert=False,
            flierprops=dict(marker='o', color='red', markersize=3)
        )

    def rolling_average(ax, indices, values, label, color):
        rolling_avg = np.convolve(
            values,
            np.ones(50)/50,
            mode='valid'
        )
        ax.plot(
            indices[49:],
            rolling_avg,
            label='Rolling Average',
            color=color
        )

    graph_map = {
            'Line': line,
            'Bar': bar,
            'Scatter': scatter,
            'Histogram': histogram,
            'Boxplot': boxplot,
            'Rolling Average': rolling_average,
    }


class GUI:
    def __init__(self, ffi: FFI, operations: dict):
        self.ffi = ffi
        self.operations = operations
        self.root = tk.Tk()

        self.root.title('Jitter Analysis')
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry('800x600')
        self.root.state('normal')

        self.operation_var = tk.StringVar()
        self.graph_type_var = tk.StringVar()
        self.metric_type_var = tk.StringVar()

        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.button_frame, width=100)

        self.graph_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.graph_frame, width=100)

        self.operation_combobox = OperationComboBox(
                self.button_frame,
                self.operations,
                textvariable=self.operation_var
                )
        self.operation_combobox.pack(pady=10)

        self.graph_type_combobox = GraphTypeComboBox(
                self.button_frame,
                textvariable=self.graph_type_var
                )
        self.graph_type_combobox.pack(pady=10)

        self.metric_type_listbox = MetricTypeListbox(self.button_frame, height=4)
        self.metric_type_listbox.pack(pady=10)

        self.iterations_entry_box = IterationsEntryBox(self.button_frame)
        self.iterations_entry_box.pack(pady=5)

        self.add_graph_button = ttk.Button(
                self.button_frame,
                text='Add Graph',
                command=self.on_add_graph
                )
        self.add_graph_button.pack(pady=10)

        self.close_button = ttk.Button(
                self.button_frame,
                text='Close',
                command=self.on_close
                )
        self.close_button.pack(pady=10)

        self.canvas = GraphCanvas(self.graph_frame)

        self.canvas.bind_all('<MouseWheel>', self.canvas.on_mouse_wheel)
        self.canvas.bind_all('<Button-4>', self.canvas.on_mouse_wheel)
        self.canvas.bind_all('<Button-5>', self.canvas.on_mouse_wheel)



    def plot_data(
        self,
        data: List[int],
        op_name: str,
        graph_type: str,
        metric_values: dict,
    ):
        indices = np.arange(len(data))
        values = [float(i) for i in data]

        fig, ax = plt.subplots(figsize=(8, 4))

        label = 'Execution time'
        color = 'blue'
        Graphs.graph_map[graph_type](ax, indices, values, label, color)

        for metric, value in metric_values.items():
            ax.axhline(
                y=value,
                color='red',
                linestyle='--',
                label=f'{metric}: {value:.2f}'
            )
            ax.annotate(
                f'{metric}: {value:.2f}',
                xy=(0, value),
                xytext=(10, value + 10),
                textcoords='offset points',
                fontsize=10,
                color='red',
                arrowprops=dict(arrowstyle='->', color='red')
            )

        ax.set_xlabel('Data Point')
        ax.set_ylabel('Difference in CPU ticks')
        ax.set_title(f'Timing difference of operation {op_name}')
        ax.legend()

        return fig

    def add_graph(
        self,
        data: List[int],
        op_name: str,
        graph_type: str,
        metric_values: dict,
    ):
        graph_frame = self.canvas.add_graph_frame()
        fig = self.plot_data(
            data,
            op_name,
            graph_type,
            metric_values
        )

        fig_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(fig_canvas, graph_frame)
        toolbar.update()
        toolbar.pack(fill=tk.X)

        close_button = ttk.Button(
                graph_frame,
                text='Close Graph',
                command=lambda: self.remove_graph(graph_frame)
                )
        close_button.pack(pady=5)

    def remove_graph(self, graph_frame):
        graph_frame.destroy()

    def on_add_graph(self):
        # Collect variables from UI elements
        selected_operation_name = self.operation_var.get()
        selected_graph_type = self.graph_type_var.get()
        selected_metrics = self.metric_type_listbox.get_selected_metrics()
        iterations = self.iterations_entry_box.get_iterations()

        # Get operation object
        selected_operation = next(
            op for op in self.operations.values()
            if op.name == selected_operation_name
        )

        # Call to C lib to perform selected operation
        data, name = selected_operation.run(
            self.ffi.lib.get_ticks_diff,
            iterations=iterations
        )

        # Compute selected metrics
        metric_values = {}
        for metric in selected_metrics:
            metric_values[metric] = Statistics.statistics_map[metric](data)

        # Pass multiple metrics to the graph
        self.add_graph(data, name, selected_graph_type, metric_values)

    def on_close(self):
        self.root.quit()
        self.root.destroy()
