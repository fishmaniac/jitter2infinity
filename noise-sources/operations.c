#include "lib.h"
#include <stdint.h>
#include <stdio.h>
#include <limits.h>

void flush_cache(void *addr) {
    __asm__ volatile (
        "clflush (%0)"
        :
        : "r" (addr)
        : "memory"
    );
}

#ifdef JENT
#include <jitterentropy-base-user.h>
#include <jitterentropy.h>
int is_init = 1;
struct rand_data *entropy_collector;

uint64_t jitter_entropy_op(uint64_t *data) {
	if (is_init != 0) {
		// Could use safe version instead?
		is_init = jent_entropy_init();
		entropy_collector = jent_entropy_collector_alloc(
			1, // Oversampling rate
			0b00000 // Flags
		);
	}
	// 8 bytes for uint64_t
	int read = jent_read_entropy(entropy_collector, (char *) data, 8);
	if (read == 8) return *data;
	else return read;
}
void cleanup_jitter_entropy(void)  {
	if (is_init == 0) {
		jent_entropy_collector_free(entropy_collector);
	}
}
#endif
void cubed_op(uint64_t *data) {
	uint64_t *x = data;
	*x = *x * *x * *x;
}
void timespec_clock_op(uint64_t *data) {
	struct timespec ts;
	*(uint64_t*) data = get_time(&ts);
}
void clock_print_op(uint64_t *data) {
	printf("num: %ld\n", get_ticks());
}
void print_op(uint64_t *data) {
	printf("\n");
}

void tsp_op(uint64_t *data) {
	// Example graph represented as an adjacency matrix
	int graph[gv_len][gv_len] = {
		{0, 3, 1, 6, 0, 0},
		{3, 0, 5, 0, 3, 0},
		{1, 5, 0, 5, 6, 4},
		{6, 0, 5, 0, 0, 2},
		{0, 3, 6, 0, 0, 6},
		{0, 0, 4, 2, 6, 0}
	};
	tsp_approximation(graph, data);
}
void tsp_dp_op(uint64_t *data) {
	*data = tsp_dp(1, 0);
}
void interrupt_op(uint64_t *data) {
    __asm__ (
        "int $0x80;"
    );
}
void get_pid_op(uint64_t *data) {
    __asm__ (
        "mov $39, %%rax;"
        "syscall;"
        "mov %%rax, %0;"
        : "=r" (*data)
        :
        : "%rax"
    );
}
void graph_color_op(uint64_t *data) {
	/* Create following graph and test
       whether it is 3 colorable
      (3)---(2)
       |   / |
       |  /  |
       | /   |
      (0)---(1)
    */
	bool graph[gv_len][gv_len] = {
		{ 0, 1, 1, 1, 0, 1 },
		{ 1, 0, 1, 0, 0, 0 },
		{ 1, 1, 0, 1, 1, 0 },
		{ 1, 0, 1, 0, 0, 0 },
		{ 0, 0, 0, 1, 0, 1 },
		{ 0, 1, 1, 0, 1, 0 },
	};
	int m = 3; // Number of colors

	*data = graph_coloring(graph, m);
}
void long_loop_op(uint64_t *data) {
	int x = 0;
	for (int i = 0; i < 100000; i++) {
		x += 1;
	}
	*data = x;
}
void rdtsc_op(uint64_t *data) {
	uint32_t low, high;
	asm volatile("rdtsc" : "=a"(low), "=d"(high));
}
