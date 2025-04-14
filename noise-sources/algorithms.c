#include "lib.h"
#include <stdbool.h>
#include <limits.h>

// https://www.tutorialspoint.com/data_structures_algorithms/dsa_travelling_salesman_approximation_algorithm.htm
int find_min_key(int key[], bool mstSet[]) {
	int min = INT_MAX, min_index;
	for (int v = 0; v < gv_len; v++) {
		if (mstSet[v] == false && key[v] < min) {
			min = key[v];
			min_index = v;
		}
	}
	return min_index;
}

void prim_MST(int graph[gv_len][gv_len], int parent[]) {
	int key[gv_len];
	bool mstSet[gv_len];
	for (int i = 0; i < gv_len; i++) {
		key[i] = INT_MAX;
		mstSet[i] = false;
	}
	key[0] = 0;
	parent[0] = -1;
	for (int count = 0; count < gv_len - 1; count++) {
		int u = find_min_key(key, mstSet);
		mstSet[u] = true;
		for (int v = 0; v < gv_len; v++) {
			if (graph[u][v] && mstSet[v] == false && graph[u][v] < key[v]) {
				parent[v] = u;
				key[v] = graph[u][v];
			}
		}
	}
}

void tsp_approximation(int graph[gv_len][gv_len], uint64_t *cost) {
	int parent[gv_len];
	int root = 0;
	prim_MST(graph, parent);

	int curr_cost = 0;
	for (int i = 1; i < gv_len; i++) {
		curr_cost += graph[parent[i]][i];
	}

	*cost = curr_cost;
}

// https://www.thecrazyprogrammer.com/2017/05/travelling-salesman-problem.html
int tsp_dp(int mark, int position) {
	int n = 4;
	int distan[20][20] = {
		{0, 22, 26, 30},
		{30, 0, 45, 35},
		{25, 45, 0, 60},
		{30, 35, 40, 0}};
	int dp[32][8];

	for (int i = 0; i < (1 << n); i++) {
		for (int j = 0; j < n; j++) {
			dp[i][j] = -1;
		}
	}

	int completed_visit = (1 << n) - 1;
	if (mark == completed_visit) {
		return distan[position][0];
	}
	if (dp[mark][position] != -1) {
		return dp[mark][position];
	}
	int answer = 9999;
	for (int city = 0; city < n; city++) {
		if ((mark & (1 << city)) == 0) {
			int newAnswer = distan[position][city] + tsp_dp(mark | (1 << city), city);
			answer = (answer < newAnswer) ? answer : newAnswer;
		}
	}
	return dp[mark][position] = answer;
}

// https://www.geeksforgeeks.org/graph-coloring-applications/
bool is_safe(int v, bool graph[gv_len][gv_len], int color[], int c) {
	for (int i = 0; i < gv_len; i++)
		if (graph[v][i] && c == color[i])
			return false;
	return true;
}

bool graph_coloring_util(bool graph[gv_len][gv_len], int m, int color[], int v) {
	if (v == gv_len)
		return true;

	for (int c = 1; c <= m; c++) {
		if (is_safe(v, graph, color, c)) {
			color[v] = c;

			if (graph_coloring_util(graph, m, color, v + 1)
				== true)
				return true;

			color[v] = 0;
		}
	}
	return false;
}

int graph_coloring(bool graph[gv_len][gv_len], int m) {
	int color[gv_len];
	for (int i = 0; i < gv_len; i++)
		color[i] = 0;

	if (graph_coloring_util(graph, m, color, 0) == false) {
		return -1;
	}

	return color[0];
}
