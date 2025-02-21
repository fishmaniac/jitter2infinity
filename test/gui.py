import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from typing import List

from ffi import FFI


class GUI:
    def __init__(self, ffi: FFI, operations: dict):
        self.ffi = ffi
        self.root = tk.Tk()
        self.root.title("Jitter Analysis")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(
                main_frame,
                orient=tk.VERTICAL,
                command=self.canvas.yview
                )

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                    )
                )

        self.canvas.create_window(
                (0, 0),
                window=self.scrollable_frame,
                anchor="nw"
                )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind_all(
                "<MouseWheel>",
                lambda event: self.on_mouse_wheel(event)
                )
        self.canvas.bind_all(
                "<Button-4>",
                lambda event: self.on_mouse_wheel(event)
                )
        self.canvas.bind_all(
                "<Button-5>",
                lambda event: self.on_mouse_wheel(event)
                )

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.operations = operations

        self.operation_var = tk.StringVar()
        operation_names = [op.name for op in operations.values()]
        self.operation_combobox = ttk.Combobox(
            self.scrollable_frame,
            values=operation_names,
            textvariable=self.operation_var,
            state="readonly"
        )
        self.operation_combobox.pack(pady=10)

        add_graph_button = ttk.Button(
            self.scrollable_frame,
            text="Add Graph",
            command=self.on_add_graph
        )
        add_graph_button.pack(pady=10)

        close_button = ttk.Button(
                self.scrollable_frame,
                text="Close",
                command=self.on_close
                )
        close_button.pack(pady=10)

        self.root.mainloop()

    def plot_data(self, data: List[int], op_name: str):
        indices = np.arange(len(data))
        values = [float(i) for i in data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(indices, values, label='Data over Time', color='blue')
        ax.set_xlabel('Data Point')
        ax.set_ylabel('Time difference in nanoseconds')
        ax.set_title(f'Timing difference of operation {op_name}')
        ax.legend()

        return fig

    def add_graph(self, data: List[int], op_name: str):
        graph_frame = tk.Frame(self.scrollable_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig = self.plot_data(data, op_name)

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

        if selected_operation_name:
            selected_operation = next(
                op for op in self.operations.values()
                if op.name == selected_operation_name
            )

            data, name = selected_operation.run(self.ffi)
            self.add_graph(data, name)

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def on_close(self):
        self.root.quit()
        self.root.destroy()
