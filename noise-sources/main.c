#include <stdio.h>

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
struct timespec ts;
// https://stackoverflow.com/a/51974214
long get_time(struct timespec ts)
{
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
#include <time.h>
struct timespec ts;
long get_time(struct timespec ts) {
	clock_gettime(CLOCK_REALTIME, &ts);
	return ts.tv_nsec;
}
#endif

void cubed_op(void *data) {
	int *x = ((int*) data);
	*x = *x * *x * *x;
}
// test ops to simulate delay
void timespec_clock_op(void *data) {
	*(long*) data = get_time(ts);
}
void clock_print_op(void *data) {
	printf("num: %ld\n", get_time(ts));
}

long get_time_diff(void (*delay_op)(void *)) {
	int data = 0;

	long ts0 = get_time(ts);

	delay_op(&data);

	long ts1 = get_time(ts);

	return (long) ts1 - ts0;
}

// int main(void) {
// 	FILE *file;
// 	file = fopen("data.dat", "w");
//
// 	if (file == NULL) {
// 		printf("Error writing file...");
// 		return -1;
// 	}
//
// 	printf("...");
//
// 	int i = 0;
// 	while (i++ < 1000000) {
// 		long diff = get_time_diff(cubed_op);
// 		printf("diff: %ld\n", diff);
// 		fprintf(file, "%ld\n", diff);
// 	}
//
// 	printf("done\n");
// }
