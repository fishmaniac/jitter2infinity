import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
import numpy as np
from enum import Enum, EnumMeta, unique
from collections import Counter
import csv
import time

from operation import OptimizationLevel, OperationType
from analysis import MetricType, Analysis


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


class RemoveOutliersCheckbox(tk.Checkbutton):
    def __init__(self, parent, *args, **kwargs):
        self.remove_outliers_var = tk.BooleanVar()
        self.remove_outliers_var.set(False)

        super().__init__(parent, variable=self.remove_outliers_var, text='Remove outliers', *args, **kwargs)

    def get(self):
        return self.remove_outliers_var.get()

class RemoveLegendCheckbox(tk.Checkbutton):
    def __init__(self, parent, *args, **kwargs):
        self.remove_legend_var = tk.BooleanVar()
        self.remove_legend_var.set(False)

        super().__init__(parent, variable=self.remove_legend_var, text='Remove legend', *args, **kwargs)

    def get(self):
        return self.remove_legend_var.get()



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
        ax.scatter(indices, values, label=label, color=color, s=5, alpha=0.3)

    def scatter_sized(ax, indices, values, label, color):
        unique_values, counts = np.unique(values, return_counts=True)
        frequency_array = counts[np.searchsorted(unique_values, values)]

        ax.scatter(indices, values, label=label, color=color, s=frequency_array, alpha=1)

    def line(ax, indices, values, label, color):
        ax.plot(indices, values, label=label, color=color)

    def bar(ax, indices, values, label, color):
        ax.bar(indices, values, label=label, color=color)

    def histogram2D(ax, indices, values, label, color):
        c = ax.hist2d(indices, values, label=label, color=color)
        fig = ax.figure
        fig.colorbar(c[3], ax=ax, label='Counts')

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

    def hexbin(ax, indices, values, label, color):
        # Create a hexbin plot to visualize dense areas
        hb = ax.hexbin(indices, values, gridsize=30)
        fig = ax.figure
        fig.colorbar(hb, ax=ax, label='Density')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Hexbin Plot')

    def violin(ax, indices, values, label, color):
        # Create a violin plot
        ax.violinplot(values, vert=False)
        ax.set_xlabel('Values')
        ax.set_ylabel('Categories')
        ax.set_title(label)
        ax.set_facecolor(color)


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
    Scatter_Sized = ('Scatter Sized', Graphs.scatter_sized)
    Line = ('Line', Graphs.line)
    Rolling_Average = ('Rolling Average', Graphs.rolling_average)
    Bar = ('Bar', Graphs.bar)
    Histogram = ('Histogram', Graphs.histogram)
    Histogram2D = ('Histogram 2D', Graphs.histogram2D)
    Boxplot = ('Boxplot', Graphs.boxplot)
    Hexbin = ('Hexbin', Graphs.hexbin)
    Violin = ('Violin', Graphs.violin)

    def __init__(self, graph_name: str, func):
        self.graph_name = graph_name
        self.func = func


# TODO: use this
class JitterStat:
    def __init(self, operation):
        self.operation = operation


class GUI:
    def __init__(self, ffi_dict: dict):
        self.root = tk.Tk()
        self.root.title('Jitter Analysis')
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry('800x600')
        self.root.state('normal')
        self.root.configure(bg='#2e2e2e')
        self.root.tk_setPalette(background='#2e2e2e', foreground='#f0f0f0')

        self.ffi_dict = ffi_dict
        self.operation_var = tk.StringVar()
        self.graph_type_var = tk.StringVar()
        self.metric_type_var = tk.StringVar()

        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.button_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.button_frame, width=150)
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

        self.remove_outliers_checkbox = RemoveOutliersCheckbox(self.button_frame, height=2)
        self.remove_outliers_checkbox.pack(pady=5)

        self.remove_legend_checkbox = RemoveLegendCheckbox(self.button_frame, height=2)
        self.remove_legend_checkbox.pack(pady=5)

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

    def save_graph_to_csv(self, data, filename='graph_data.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            header = ['Time Point']
            for entry in data:
                optimization_level = entry['optimization_level'].level
                header.append(optimization_level)

            writer.writerow(header)

            max_time_diff_length = max(
                    len(entry['time_diff']) for entry in data
                    )

            for i in range(max_time_diff_length):
                row = [i]
                for entry in data:
                    time_diffs = entry['time_diff']
                    if i < len(time_diffs):
                        row.append(time_diffs[i])
                    else:
                        row.append('')
                writer.writerow(row)

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

            # Run selected operation
            time_diffs = operation.run(ffi, iterations)

            # Remove outliers
            if self.remove_outliers_checkbox.get():
                print("Removing outliers...")
                time_diffs = Analysis.remove_outliers_iqr(time_diffs)

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

        self.save_graph_to_csv(
                data,
                ''.join((
                    f'''graph-{selected_operation_name}-{selected_graph_type}
                    -{time.time_ns()}.csv''').split())
                )
        self.add_graph(data, selected_operation_name)

    def add_graph(self, data, selected_operation_name: str):
        graph_frame = self.canvas.add_graph_frame()

        fig = self.plot_data(data, selected_operation_name)

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

    def plot_data(self, data, selected_operation_name: str):
        fig, ax = plt.subplots(figsize=(12, 8))
        legend_lines = []

        while data:
            entry = data.pop(0)

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
                        label=f'''{metric_name}: {metric_value:.2f} | {
                            optimization_level.level
                        }'''
                        )
                legend_lines.append(legend_line)

        ax.set_xlabel('Data Point')
        ax.set_ylabel('Difference in CPU ticks')
        ax.set_title(f'''Timing difference of operation {
            selected_operation_name
        }''')

        # Remove legend
        if not self.remove_legend_checkbox.get():
            ax.legend(handles=legend_lines, loc='upper right')

        return fig

    def remove_graph(self, graph_frame):
        graph_frame.destroy()

    def on_close(self):
        self.root.quit()
        self.root.destroy()
