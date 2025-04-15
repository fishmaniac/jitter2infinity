from gui import GUI
from ffi import FFI
from operation import OptimizationLevel


def main():
    cdef = """
        uint64_t get_time_diff(void (*delay_op)(uint64_t *));
        uint64_t get_ticks_diff(void (*delay_op)(uint64_t *));
        void flush_cache(void *addr);
        void cubed_op(uint64_t *data);
        void timespec_clock_op(uint64_t *data);
        void clock_print_op(uint64_t *data);
        void print_op(uint64_t *data);
        void interrupt_op(uint64_t *data);
        void get_pid_op(uint64_t *data);
        void tsp_dp_op(uint64_t *data);
        void tsp_op(uint64_t *data);
        void graph_color_op(uint64_t *data);
        void long_loop_op(uint64_t *data);
        void rdtsc_op(uint64_t *data);
        uint64_t jitter_entropy_op(uint64_t *data);
        """

    ffi_dict = {}
    for level in OptimizationLevel:
        ffi_dict[level.name] = FFI(
            cdef=cdef,
            lib_name=f'jitter2infinitylib{level.level}',
        )

    # operations = Operation.base_operations(
    #     ffi_dict=ffi_dict
    # )

    # for level, ffi in ffi_dict.items():
    #     operations.update()

    GUI(ffi_dict)


if __name__ == '__main__':
    main()
