#include "lib.h"
#include <stdio.h>

void cubed_op(void *data) {
	int *x = ((int*) data);
	*x = *x * *x * *x;
}
void timespec_clock_op(void *data) {
	*(long*) data = get_time(ts);
}
void clock_print_op(void *data) {
	printf("num: %ld\n", get_time(ts));
}
