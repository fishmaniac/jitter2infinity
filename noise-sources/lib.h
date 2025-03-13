#include <stdint.h>
#define NS_PER_SEC 1000000000
#ifdef _WIN32
#include <windows.h>
struct timespec {
	uint64_t tv_sec;
	uint64_t tv_nsec;
};
#elif defined(__linux__)
#include <time.h>
#endif

// TODO:
// bubble sort with different array sizes
// - maybe use ratio between size/speed as rand num?
// traveling salesman approx
// other NP-hard approx?

// timer.c
uint64_t get_time(struct timespec *ts);
uint64_t get_ticks();
uint64_t get_time_diff(void (*delay_op)(uint64_t *));
uint64_t get_ticks_diff(void (*delay_op)(uint64_t *));

// operations.c
void cubed_op(uint64_t *data);
void timespec_clock_op(uint64_t *data);
void clock_print_op(uint64_t *data);
