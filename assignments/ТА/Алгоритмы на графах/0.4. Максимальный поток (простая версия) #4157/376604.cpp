#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Edge {
  int to, flow, cap, rev;
};

vector<vector<Edge>> graph;
vector<int> levels;

int dfs(int v, int t, int bottleneck) {
  if (!bottleneck) {
    return 0;
  }
  if (v == t) {
    return bottleneck;
  }

  for (auto& e : graph[v]) {
    if (levels[e.to] != levels[v] + 1) {
      continue;
    }

    int new_bottleneck = min(bottleneck, e.cap - e.flow);
    int increment = dfs(e.to, t, new_bottleneck);
    if (increment) {
      e.flow += increment;
      graph[e.to][e.rev].flow -= increment;
      return increment;
    }
  }
  return 0;
}

bool bfs(int s, int t) {
  fill(levels.begin(), levels.end(), -1);
  levels[s] = 0;
  queue<int> q;
  q.push(s);

  while (!q.empty()) {
    int v = q.front();
    q.pop();

    for (auto& e : graph[v]) {
      if (levels[e.to] < 0 && e.cap > e.flow) {
        levels[e.to] = levels[v] + 1;
        q.push(e.to);
      }
    }
  }

  return levels[t] != -1;
}

int dinic(int s, int t) {
  int flow = 0;

  while (bfs(s, t)) {
    int flow_incr;
    while (flow_incr = dfs(s, t, INT32_MAX)) {
      flow += flow_incr;
    }
  }

  return flow;
}

void add_edge(int u, int v, int w) {
  // check if edge already exists
  for (auto& e : graph[u]) {
    if (e.to == v) {
      e.cap += w;
      return;
    }
  }

  int u_size = graph[u].size();
  int v_size = graph[v].size();
  graph[u].push_back({v, 0, w, v_size});
  graph[v].push_back({u, 0, 0, u_size});
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  // ifstream cin("input.txt");

  int n, m;
  cin >> n >> m;
  graph = vector<vector<Edge>>(n);
  levels = vector<int>(n);

  int u, v, w;
  for (int i = 0; i < m; ++i) {
    cin >> u >> v >> w;
    add_edge(u - 1, v - 1, w);
  }

  cout << dinic(0, n - 1) << endl;
  return 0;
}
