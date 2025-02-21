import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from typing import List
from ffi import FFI


class OperationComboBox(ttk.Combobox):
    def __init__(self, parent, operations, *args, **kwargs):
        operation_names = [op.name for op in operations.values()]
        super().__init__(
            parent,
            values=operation_names,
            state="readonly",
            *args,
            **kwargs
        )


class GraphTypeComboBox(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            values=[
                "Scatter",
                "Line",
                "Bar",
                "Histogram",
                "Boxplot",
                "Rolling Average",
            ],
            state="readonly",
            *args,
            **kwargs
        )


class GraphCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrollbar = ttk.Scrollbar(
            parent,
            orient=tk.VERTICAL,
            command=self.yview
        )
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.bind("<Configure>", self.on_configure)

        self.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_configure(self, event):
        self.configure(scrollregion=self.bbox("all"))

    def add_graph_frame(self):
        graph_frame = tk.Frame(self.scrollable_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        return graph_frame

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.yview_scroll(-1, "units")


class GUI:
    def __init__(self, ffi: FFI, operations: dict):
        self.ffi = ffi
        self.operations = operations
        self.root = tk.Tk()

        self.root.title("Jitter Analysis")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("800x600")
        self.root.state("zoomed")

        self.operation_var = tk.StringVar()
        self.graph_type_var = tk.StringVar()

        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(paned_window)
        paned_window.add(button_frame, width=100)

        graph_frame = tk.Frame(paned_window)
        paned_window.add(graph_frame, width=100)

        self.operation_combobox = OperationComboBox(
                button_frame,
                self.operations,
                textvariable=self.operation_var
                )
        self.operation_combobox.pack(pady=10)

        self.graph_type_combobox = GraphTypeComboBox(
                button_frame,
                textvariable=self.graph_type_var
                )
        self.graph_type_combobox.pack(pady=10)

        self.add_graph_button = ttk.Button(
                button_frame,
                text="Add Graph",
                command=self.on_add_graph
                )
        self.add_graph_button.pack(pady=10)

        self.close_button = ttk.Button(
                button_frame,
                text="Close",
                command=self.on_close
                )
        self.close_button.pack(pady=10)

        self.canvas = GraphCanvas(graph_frame)
        self.canvas.bind_all("<MouseWheel>", self.canvas.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.canvas.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.canvas.on_mouse_wheel)

    def plot_data(self, data: List[int], op_name: str, graph_type: str):
        indices = np.arange(len(data))
        values = [float(i) for i in data]

        fig, ax = plt.subplots(figsize=(8, 4))

        label = 'Execution time'
        color = 'fuschia'
        if graph_type == "Line":
            ax.plot(
                indices,
                values,
                label=label,
                color=color
            )
        elif graph_type == "Bar":
            ax.bar(
                indices,
                values,
                label=label,
                color=color
            )
        elif graph_type == "Scatter":
            ax.scatter(
                indices,
                values,
                label=label,
                color=color,
                s=10
            )
        elif graph_type == "Histogram":
            ax.hist(
                values,
                label=label,
                bins=20,
                color=color,
                alpha=0.7
            )
            ax.set_xlabel('Time difference in nanoseconds')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Histogram of Timing Differences for {op_name}')
        elif graph_type == "Boxplot":
            ax.boxplot(
                values,
                label=label,
                vert=False,
                flierprops=dict(marker='o', color='red', markersize=3),
            )
            ax.set_xlabel('Time difference in nanoseconds')
            ax.set_title(f'Boxplot of Timing Differences for {op_name}')
        elif graph_type == "Rolling Average":
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

        ax.set_xlabel('Data Point')
        ax.set_ylabel('Time difference in nanoseconds')
        ax.set_title(f'Timing difference of operation {op_name}')
        ax.legend()

        return fig

    def add_graph(self, data: List[int], op_name: str, graph_type: str):
        graph_frame = self.canvas.add_graph_frame()
        fig = self.plot_data(data, op_name, graph_type)

        fig_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(fig_canvas, graph_frame)
        toolbar.update()
        toolbar.pack(fill=tk.X)

        close_button = ttk.Button(
                graph_frame,
                text="Close Graph",
                command=lambda: self.remove_graph(graph_frame)
                )
        close_button.pack(pady=5)

    def remove_graph(self, graph_frame):
        graph_frame.destroy()

    def on_add_graph(self):
        selected_operation_name = self.operation_var.get()
        selected_graph_type = self.graph_type_var.get()

        if selected_operation_name and selected_graph_type:
            selected_operation = next(
                    op for op in self.operations.values()
                    if op.name == selected_operation_name
                    )
            data, name = selected_operation.run(self.ffi)
            self.add_graph(data, name, selected_graph_type)

    def on_close(self):
        self.root.quit()
        self.root.destroy()
