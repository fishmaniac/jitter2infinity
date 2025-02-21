#include "lib.h"

struct timespec ts;

#ifdef _WIN32
// https://stackoverflow.com/a/51974214
long get_time(struct timespec ts) {
    FILETIME ft;
    ULARGE_INTEGER hnsTime;

    GetSystemTimePreciseAsFileTime(&ft);

    hnsTime.LowPart = ft.dwLowDateTime;
    hnsTime.HighPart = ft.dwHighDateTime;
    hnsTime.QuadPart -= (11644473600ULL * HNS_PER_SEC);

    ts.tv_nsec = (long) ((hnsTime.QuadPart % HNS_PER_SEC) * NS_PER_HNS);
    ts.tv_sec = (long) (hnsTime.QuadPart / HNS_PER_SEC);

    return ts.tv_nsec;
}
#elif defined(__linux__)
long get_time(struct timespec ts) {
	clock_gettime(CLOCK_REALTIME, &ts);
	return ts.tv_nsec;
}
#endif

long get_time_diff(void (*delay_op)(void *)) {
	int data = 0;

	long ts0 = get_time(ts);

	delay_op(&data);

	long ts1 = get_time(ts);

	return (long) ts1 - ts0;
}
