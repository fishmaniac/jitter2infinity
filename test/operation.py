from ffi import FFI
import numpy as np

class Operation:
    def __init__(self, ffi: FFI, name='Unknown'):
        self.ffi = ffi
        self.name = name

    def run(self, lib_counter_func: FFI, iterations=100):
        time_diffs = []
        for i in range(0, iterations):
            diff = lib_counter_func(self.ffi)
            time_diffs.append(diff)
        return time_diffs, self.name
