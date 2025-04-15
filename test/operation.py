from ffi import FFI
from enum import Enum, EnumMeta, unique


class OptimizationLevel(Enum):
    O0 = ('-O0', 'blue')
    O1 = ('-O1', 'red')
    O2 = ('-O2', 'green')
    O3 = ('-O3', 'purple')
    OFAST = ('-Ofast', 'orange')
    OG = ('-Og', 'black')
    OS = ('-Os', 'pink')

    def __init__(self, optimization_level: str, color: str):
        self.level = optimization_level
        self.color = color


class OperationTypeMeta(EnumMeta):
    def __getitem__(self, operation_name: str):
        for member in self:
            if member.operation_name == operation_name:
                return member
        raise KeyError(f"OperationType with name '{operation_name}' not found.")


@unique
class OperationType(Enum, metaclass=OperationTypeMeta):
    CUBED_OP = (
        'cubed_op',
        'get_ticks_diff',
        'Cubed'
    )
    TIMESPEC_CLOCK_OP = (
        'timespec_clock_op',
        'get_ticks_diff',
        'Timespec Clock'
    )
    CLOCK_PRINT_OP = (
        'clock_print_op',
        'get_ticks_diff',
        'Clock Print'
    )
    PRINT_OP = (
        'print_op',
        'get_ticks_diff',
        'Print'
    )
    INTERRUPT_OP = (
        'interrupt_op',
        'get_ticks_diff',
        'Interrupt'
    )
    GET_PID_OP = (
        'get_pid_op',
        'get_ticks_diff',
        'Get PID'
    )
    TSP_OP = (
        'tsp_op',
        'get_ticks_diff',
        'Traveling Salesman Approximation'
    )
    TSP_DP_OP = (
        'tsp_dp_op',
        'get_ticks_diff',
        'DP Traveling Salesman Approximation'
    )
    GRAPH_COLOR_OP = (
        'graph_color_op',
        'get_ticks_diff',
        'Graph Coloring'
    )
    LONG_LOOP_OP = (
        'long_loop_op',
        'get_ticks_diff',
        'Long Loop'
    )
    RDTSC_OP = (
        'rdtsc_op',
        'get_ticks_diff',
        'RDTSC'
    )
    # JITTER_ENTROPY_LIBRARY = (
    #     None,
    #     'get_ticks_diff',
    #     'Jitter Entropy Lib'
    # )

    def __init__(
        self,
        operation_cdef: str,
        measure_cdef: str,
        operation_name: str
    ):
        self.operation_cdef = operation_cdef
        self.measure_cdef = measure_cdef
        self.operation_name = operation_name

    def run(self, ffi: FFI, iterations=100, flush=False):
        time_diffs = []
        for i in range(0, iterations):
            ffi_func = getattr(ffi.lib, self.operation_cdef)

            diff = ffi.lib.get_ticks_diff(ffi_func)
            time_diffs.append(diff)
            if flush:
                print("flushing...")
                ffi.lib.flush_cache(ffi_func)

        return time_diffs
