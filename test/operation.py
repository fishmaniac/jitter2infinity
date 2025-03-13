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
        self.optimization_level = optimization_level
        self.color = color


class OperationTypeMeta(EnumMeta):
    def __getitem__(self, operation_name: str):
        for member in self:
            if member.operation_name == operation_name:
                return member
        raise KeyError(f"OperationType with name '{operation_name}' not found.")


@unique
class OperationType(Enum, metaclass=OperationTypeMeta):
    CUBED_OP = ('cubed_op', 'Cubed')
    TIMESPEC_CLOCK_OP = ('timespec_clock_op', 'Timespec Clock')
    CLOCK_PRINT_OP = ('clock_print_op', 'Clock Print')

    def __init__(self, cdef, operation_name: str):
        self.cdef = cdef
        self.operation_name = operation_name

    def run(self, ffi: FFI, iterations=100):
        time_diffs = []
        for i in range(0, iterations):
            ffi_func = getattr(ffi.lib, self.cdef)

            diff = ffi.lib.get_ticks_diff(ffi_func)
            time_diffs.append(diff)

        return time_diffs
