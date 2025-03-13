#include "lib.h"
#include <stdint.h>
#include <stdio.h>

void cubed_op(uint64_t *data) {
	uint64_t *x = ((uint64_t*) data);
	*x = *x * *x * *x;
}
void timespec_clock_op(uint64_t *data) {
	struct timespec ts;
	*(uint64_t*) data = get_time(&ts);
}
void clock_print_op(uint64_t *data) {
	printf("num: %ld\n", get_ticks());
}
