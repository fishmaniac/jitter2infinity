from ffi import FFI


class Operation:
    def __init__(self, ffi, iterations=100, name="Unknown"):
        self.ffi = ffi
        self.iterations = iterations
        self.name = name

    def run(self, ffi: FFI):
        time_diffs = []
        for i in range(0, self.iterations):
            diff = ffi.lib.get_time_diff(self.ffi)
            time_diffs.append(diff)
        return time_diffs, self.name
