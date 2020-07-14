#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

using ll = long long;

struct Edge {
  ll to, weight;
};

vector<ll> visited;

vector<ll> restore_path(vector<ll>& visit_history, ll s, ll e) {
  if (visit_history[e] < 0) {
    return vector<ll>();
  }

  vector<ll> path(1, e);
  ll curr = e;
  while (visit_history[curr] != curr) {
    curr = visit_history[curr];
    path.push_back(curr);
  }
  reverse(path.begin(), path.end());
  return std::move(path);
}

vector<ll> bfs(vector<vector<Edge>>& graph, ll s, ll e) {
  fill(visited.begin(), visited.end(), -1);
  queue<ll> q;
  q.push(s);
  visited[s] = s;

  while (!q.empty()) {
    ll v = q.front();
    q.pop();

    if (v == e) {
      break;
    }

    for (auto& adj_v : graph[v]) {
      if (visited[adj_v.to] < 0 && adj_v.weight > 0) {
        q.push(adj_v.to);
        visited[adj_v.to] = v;
      }
    }
  }

  return std::move(restore_path(visited, s, e));
}

ll find_bottleneck(vector<vector<Edge>>& graph, vector<ll>& path) {
  ll bottleneck = __LONG_LONG_MAX__;
  for (ll i = 0; i < path.size() - 1; ++i) {
    for (auto& next : graph[path[i]]) {
      if (next.to == path[i + 1]) {
        bottleneck = min(bottleneck, next.weight);
        break;
      }
    }
  }
  return bottleneck;
}

ll update_graph(vector<vector<Edge>>& graph, vector<ll>& path) {
  ll bottleneck = find_bottleneck(graph, path);

  for (ll i = 0; i < path.size() - 1; ++i) {
    for (auto& next : graph[path[i]]) {
      if (next.to == path[i + 1]) {
        next.weight -= bottleneck;
        break;
      }
    }
  }

  for (ll i = path.size() - 1; i > 0; --i) {
    for (auto& prev : graph[path[i]]) {
      if (prev.to == path[i - 1]) {
        prev.weight += bottleneck;
        break;
      }
    }
  }

  return bottleneck;
}

bool edge_exists(vector<vector<Edge>>& graph, ll s, ll e) {
  for (auto& edge : graph[s]) {
    if (edge.to == e) return true;
  }
  return false;
}

vector<vector<Edge>> build_adj_graph(vector<vector<Edge>>& graph) {
  vector<vector<Edge>> adj_graph(graph.size());
  for (ll from = 0; from < graph.size(); ++from) {
    for (auto& edge : graph[from]) {
      adj_graph[from].push_back({edge.to, edge.weight});
      if (!edge_exists(graph, edge.to, from)) {
        adj_graph[edge.to].push_back({from, 0});
      }
    }
  }

  return std::move(adj_graph);
}

ll max_flow(vector<vector<Edge>>& graph, ll s, ll e) {
  vector<vector<Edge>> adj_graph = build_adj_graph(graph);
  vector<ll> path;
  ll flow = 0;
  while (!(path = bfs(adj_graph, s, e)).empty()) {
    flow += update_graph(adj_graph, path);
  }
  return flow;
}

struct mapper {
  vector<int> ar;
  int num;

  mapper(int n) : ar(n, -1), num(0) {}

  int get(int x) {
    if (ar[x] == -1) ar[x] = num++;
    return ar[x];
  }

  size_t size() { return num; }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  // ifstream cin("input.txt");

  vector<vector<Edge>> graph;
  ll n, m;
  // n -- vertices
  // m -- edges
  cin >> n >> m;
  graph = vector<vector<Edge>>(n);

  visited = vector<ll>(n);

  mapper mo(n);

  int s = mo.get(0);
  int e = mo.get(n - 1);

  for (ll i = 0; i < m; ++i) {
    ll u, v, w;
    cin >> u >> v >> w;
    u = mo.get(u - 1);
    v = mo.get(v - 1);

    for (auto& vert : graph[u]) {
      if (vert.to == v) {
        vert.weight += w;
        w = 0;
        break;
      }
    }

    if (w > 0) graph[u].push_back({v, w});
  }

  n = mo.size();
  graph.shrink_to_fit();

  cout << max_flow(graph, s, e) << endl;

  return 0;
}