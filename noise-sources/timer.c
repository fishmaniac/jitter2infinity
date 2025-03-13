#include "lib.h"
#include <stdint.h>

// todo: use rdtsc
// https://learn.microsoft.com/en-us/cpp/intrinsics/rdtsc?view=msvc-170

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
	return ((uint64_t)high << 32) | low;
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

uint64_t get_ticks_diff(void (*delay_op)(uint64_t *)) {
	uint64_t data = 0x123;
	struct timespec ts;

	uint64_t ts0 = get_ticks();

	delay_op(&data);

	uint64_t ts1 = get_ticks();

	return ts1 - ts0;
}
