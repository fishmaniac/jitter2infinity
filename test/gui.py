import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
import numpy as np
from enum import Enum, EnumMeta, unique

from operation import OptimizationLevel, OperationType
from analysis import MetricType


class OperationComboBox(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        ops = [op.operation_name for op in OperationType]
        super().__init__(parent, values=ops, state='readonly', *args, **kwargs)


class GraphTypeComboBox(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        graphs = [graph.graph_name for graph in GraphType]
        super().__init__(parent, values=graphs, state='readonly', *args, **kwargs)


class MetricTypeListbox(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, selectmode=tk.MULTIPLE, exportselection=False, *args, **kwargs)
        for metric in MetricType:
            self.insert(tk.END, metric.metric_name)

    def get_selected_metrics(self):
        return [self.get(i) for i in self.curselection()]


class OptimizationTypeListbox(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, selectmode=tk.MULTIPLE, exportselection=False, *args, **kwargs)
        for optimization in OptimizationLevel:
            self.insert(tk.END, optimization.name)

    def get_selected_optimizations(self):
        return [self.get(i) for i in self.curselection()]


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


class Graphs:
    def scatter(ax, indices, values, label, color):
        ax.scatter(indices, values, label=label, color=color, s=5, alpha=1)

    def scatter_light(ax, indices, values, label, color):
        ax.scatter(indices, values, label=label, color=color, s=5, alpha=0.2)

    def line(ax, indices, values, label, color):
        ax.plot(indices, values, label=label, color=color)

    def bar(ax, indices, values, label, color):
        ax.bar(indices, values, label=label, color=color)

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
        rolling_avg = np.convolve(values, np.ones(50) / 50, mode='valid')
        ax.plot(
            indices[49:],
            rolling_avg,
            label='Rolling Average Execution Time',
            color=color
        )


class GraphTypeMeta(EnumMeta):
    def __getitem__(self, graph_name: str):
        for member in self:
            if member.graph_name == graph_name:
                return member
        raise KeyError(f"GraphType with name '{graph_name}' not found.")


@unique
class GraphType(Enum, metaclass=GraphTypeMeta):
    Scatter = ('Scatter', Graphs.scatter)
    Scatter_Light = ('Scatter Light', Graphs.scatter_light)
    Line = ('Line', Graphs.line)
    Rolling_Average = ('Rolling Average', Graphs.rolling_average)
    Bar = ('Bar', Graphs.bar)
    Histogram = ('Histogram', Graphs.histogram)
    Boxplot = ('Boxplot', Graphs.boxplot)

    def __init__(self, graph_name: str, func):
        self.graph_name = graph_name
        self.func = func


# TODO: use this
class JitterStat:
    def __init(self, operation):
        self.operation = operation


class GUI:
    def __init__(self, ffi_dict: dict):
        self.ffi_dict = ffi_dict
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

        self.operation_combobox = OperationComboBox(self.button_frame, textvariable=self.operation_var)
        self.operation_combobox.pack(pady=10)

        self.graph_type_combobox = GraphTypeComboBox(
            self.button_frame,
            textvariable=self.graph_type_var
        )
        self.graph_type_combobox.pack(pady=10)

        self.optimization_type_listbox = OptimizationTypeListbox(self.button_frame, height=4)
        self.optimization_type_listbox.pack(pady=10)

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

    def on_add_graph(self):
        selected_operation_name = self.operation_var.get()
        selected_graph_type = self.graph_type_var.get()
        selected_metrics = self.metric_type_listbox.get_selected_metrics()
        selected_optimizations = self.optimization_type_listbox.get_selected_optimizations()
        iterations = self.iterations_entry_box.get_iterations()
        graph = GraphType[selected_graph_type]

        data = []
        print('Selected: ', selected_optimizations)
        for optimization_level in selected_optimizations:
            operation = OperationType[selected_operation_name]
            ffi = self.ffi_dict[optimization_level]

            time_diffs = operation.run(ffi, iterations)

            metrics = []
            for selected_metric in selected_metrics:
                metric = MetricType[selected_metric]
                metrics.append({
                    'name': metric.metric_name,
                    'func': metric.func(time_diffs)
                })

            data.append({
                'time_diff': time_diffs,
                'metrics': metrics,
                'graph': graph,
                'optimization_level': OptimizationLevel[optimization_level]
                })

        self.add_graph(data)

    def add_graph(self, data):
        graph_frame = self.canvas.add_graph_frame()
        fig = self.plot_data(data)
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

    def plot_data(self, data):
        fig, ax = plt.subplots(figsize=(12, 8))
        legend_lines = []

        for entry in data:
            time_diffs = entry['time_diff']
            metrics = entry['metrics']
            graph = entry['graph']
            optimization_level = entry['optimization_level']

            color = optimization_level.color
            indices = np.arange(len(time_diffs))

            graph.func(ax, indices, time_diffs, label='test', color=color)

            for metric in metrics:
                metric_value = metric['func']
                metric_name = metric['name']

                legend_line = Line2D(
                    [0],
                    [0],
                    color=color,
                    linestyle='--',
                    label=f'{metric_name}: {metric_value:.2f} - {optimization_level}'
                )
                legend_lines.append(legend_line)

        ax.set_xlabel('Data Point')
        ax.set_ylabel('Difference in CPU ticks')
        ax.set_title(f'Timing difference of operation {optimization_level}')
        ax.legend(handles=legend_lines)

        return fig

    def on_close(self):
        self.root.quit()
        self.root.destroy()
