#ifdef _WIN32
#include <windows.h>
#define MS_PER_SEC      1000ULL
#define US_PER_MS       1000ULL
#define HNS_PER_US      10ULL
#define NS_PER_US       1000ULL
#define HNS_PER_SEC     (MS_PER_SEC * US_PER_MS * HNS_PER_US)
#define NS_PER_HNS      (100ULL)

struct timespec {
	long tv_sec;
	long tv_nsec;
};
#elif defined(__linux__)
#include <time.h>
#endif

extern struct timespec ts;

// timer.c
long get_time(struct timespec ts);
long get_time_diff(void (*delay_op)(void *));

// operations.c
void cubed_op(void *data);
void timespec_clock_op(void *data);
void clock_print_op(void *data);
