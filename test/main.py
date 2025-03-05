# internal library
from gui import GUI
from ffi import FFI
from operation import Operation


def main():
    ffi = FFI(
              """
              uint64_t get_time_diff(void (*delay_op)(void *));
              uint64_t get_ticks_diff(void (*delay_op)(void *));
              void cubed_op(void *data);
              void timespec_clock_op(void *data);
              void clock_print_op(void *data);
              """)

    operations = {
            'cubed_op': Operation(
                ffi=ffi.lib.cubed_op,
                name='Cubed'
                ),
            'timespec_clock_op': Operation(
                ffi=ffi.lib.timespec_clock_op,
                name='Timespec Clock'
                ),
            'clock_print_op': Operation(
                ffi=ffi.lib.clock_print_op,
                name='Clock Print'
                )
            }

    GUI(ffi=ffi, operations=operations)


if __name__ == "__main__":
    main()

# def check_duplicates(data):
#     map = {}
#     duplicates = 0
#     len = 0
#     for i in data:
#         len += 1
#         if i in map:
#             duplicates += 1
#             map[i] += 1
#         else:
#             map[i] = 0
#     print(f"Duplicates: {duplicates} / {len} = {duplicates/len * 100:.6f} %")
#
#
# def read_file(path):
#     with open(path, 'r') as f:
#         for line in f:
#             yield line.strip()
#
# file = "noise-sources/data.dat"
# data = list(read_file(file))
#
# check_duplicates(data)
