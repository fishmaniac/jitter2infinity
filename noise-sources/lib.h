#include <stdint.h>
#define NS_PER_SEC 1000000000
#ifdef _WIN32
#include <windows.h>
struct timespec {
	long tv_sec;
	long tv_nsec;
};
#elif defined(__linux__)
#include <time.h>
#endif

// timer.c
uint64_t get_time(struct timespec *ts);
uint64_t get_ticks();
uint64_t get_time_diff(void (*delay_op)(void *));
uint64_t get_ticks_diff(void (*delay_op)(void *));

// operations.c
void cubed_op(void *data);
void timespec_clock_op(void *data);
void clock_print_op(void *data);
