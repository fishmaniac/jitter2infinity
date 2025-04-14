#ifndef JITTER2INFINITY_LIB_H
#define JITTER2INFINITY_LIB_H

#include <stdint.h>
#include <stdbool.h>
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
#ifdef JENT
#include <jitterentropy-base-user.h>
#include <jitterentropy.h>
uint64_t jitter_entropy_op(uint64_t *data);
void cleanup_jitter_entropy() __attribute__((destructor));
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
void interrupt_op(uint64_t *data);
void get_pid_op(uint64_t *data);
void tsp_dp_op(uint64_t *data);
void tsp_op(uint64_t *data);
void graph_color_op(uint64_t *data);
void long_loop_op(uint64_t *data);
void rdtsc_op(uint64_t *data);

// algorithms.c

/* TSP greedy */
#define gv_len 6
int find_min_key(int key[], bool mstSet[]);
void prim_MST(int graph[gv_len][gv_len], int parent[]);
void tsp_approximation(int graph[gv_len][gv_len], uint64_t *cost);

/* TSP DP */
int tsp_dp(int mark, int position);

/* Graph Coloring */
bool is_safe(int v, bool graph[gv_len][gv_len], int color[], int c);
bool graph_coloring_util(bool graph[gv_len][gv_len], int m, int color[], int v);
int graph_coloring(bool graph[gv_len][gv_len], int m);

#endif  // JITTER2INFINITY_LIB_H
