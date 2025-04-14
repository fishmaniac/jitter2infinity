#include "lib.h"
#include <stdint.h>

#ifdef _WIN32
uint64_t get_time(struct timespec *ts) {
	LARGE_INTEGER elapsed;
	LARGE_INTEGER frequency;

	QueryPerformanceFrequency(&frequency);
	QueryPerformanceCounter(&elapsed);

	elapsed.QuadPart *= NS_PER_SEC;
	elapsed.QuadPart /= frequency.QuadPart;

	return (uint64_t) elapsed.QuadPart;
}

uint64_t get_ticks() {
	return (uint64_t) __rdtsc();
}

#elif defined(__linux__)
uint64_t get_time(struct timespec *ts) {
	clock_gettime(CLOCK_MONOTONIC_RAW, ts);
	return (ts->tv_sec * NS_PER_SEC) + ts->tv_nsec;
}

uint64_t get_ticks() {
	uint32_t low, high;
	asm volatile("rdtsc" : "=a"(low), "=d"(high));
	return ((uint64_t) high << 32) | low;
}
#endif

uint64_t get_time_diff(void (*delay_op)(uint64_t *)) {
	uint64_t data = 0x123;
	struct timespec ts;

	uint64_t ts0 = get_time(&ts);

	delay_op(&data);

	uint64_t ts1 = get_time(&ts);

	return ts1 - ts0;
}

#ifdef TRACEPOINTS
#include <linux/tracepoint.h>
TRACEPOINT_EVENT(
    get_ticks_diff_tracepoint,
    get_ticks_diff_start,
    TP_ARGS(uint64_t, ts0),
    TP_FIELDS(CTF_UINT64(ts0, ts0))
);

TRACEPOINT_EVENT(
    get_ticks_diff_tracepoint,
    get_ticks_diff_end,
    TP_ARGS(uint64_t, ts1),
    TP_FIELDS(CTF_UINT64(ts1, ts1))
);
#endif

uint64_t get_ticks_diff(void (*delay_op)(uint64_t *)) {
	uint64_t data = 0x123;
	struct timespec ts;

	uint64_t ts0 = get_ticks();
	#ifdef TRACEPOINTS
	trace_my_tracepoint(get_ticks_diff_start, ts0);
	#endif

	delay_op(&data);

	uint64_t ts1 = get_ticks();
	#ifdef TRACEPOINTS
	trace_my_tracepoint(get_ticks_diff_end, ts1)
	#endif

	return ts1 - ts0;
}
