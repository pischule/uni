#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

using ll = long long;

const ll INF = __LONG_LONG_MAX__;

struct Edge {
  ll to, flow, cap, rev;
};

vector<vector<Edge>> graph;
vector<int> levels;
vector<int> next_e;
int n, m;
int s, t;

ll dfs(int v, ll flow) {
  if (v == t) {
    return flow;
  }
  int edges_number = graph[v].size();
  Edge* e;

  while (next_e[v] < edges_number) {
    e = &graph[v][next_e[v]];
    ll rem_cap = e->cap - e->flow;

    if (rem_cap > 0 && levels[e->to] == levels[v] + 1) {
      ll new_bottleneck = dfs(e->to, min(flow, rem_cap));
      if (new_bottleneck > 0) {
        e->flow += new_bottleneck;
        graph[e->to][e->rev].flow -= new_bottleneck;

        return new_bottleneck;
      }
    }

    ++next_e[v];
  }

  return 0;
}

bool bfs() {
  fill(levels.begin(), levels.end(), -1);
  levels[s] = 0;
  queue<int> q;
  q.push(s);
  int cap;
  while (!q.empty()) {
    int v = q.front();
    q.pop();

    for (auto& e : graph[v]) {
      cap = e.cap - e.flow;
      if (levels[e.to] == -1 && cap > 0) {
        levels[e.to] = levels[v] + 1;
        q.push(e.to);
      }
    }
  }

  return levels[t] != -1;
}

ll dinic(ll s, ll t) {
  ll flow = 0;
  ll flow_incr;

  while (bfs()) {
    fill(next_e.begin(), next_e.end(), 0);
    while (flow_incr = dfs(s, __LONG_LONG_MAX__)) {
      flow += flow_incr;
    }
  }

  return flow;
}

void add_edge(ll u, ll v, ll w) {
  // check if edge already exists
  for (auto& e : graph[u]) {
    if (e.to == v) {
      e.cap += w;
      return;
    }
  }

  ll u_size = graph[u].size();
  ll v_size = graph[v].size();
  graph[u].push_back({v, 0, w, v_size});
  graph[v].push_back({u, 0, 0, u_size});
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  // ifstream cin("input.txt");

  cin >> n >> m;
  graph = vector<vector<Edge>>(n);
  levels = vector<int>(n);
  next_e = vector<int>(n);
  s = 0;
  t = n - 1;

  ll u, v, w;
  for (ll i = 0; i < m; ++i) {
    cin >> u >> v >> w;
    add_edge(u - 1, v - 1, w);
  }

  cout << dinic(0, n - 1) << endl;
  return 0;
}