#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Edge {
  int to, weight;
};

vector<int> restore_path(vector<int>& visit_history, int s, int e) {
  if (visit_history[e] < 0) {
    return vector<int>();
  }

  vector<int> path(1, e);
  int curr = e;
  while (visit_history[curr] != curr) {
    curr = visit_history[curr];
    path.push_back(curr);
  }
  reverse(path.begin(), path.end());
  return std::move(path);
}

vector<int> bfs(vector<vector<Edge>>& graph, int s, int e) {
  vector<int> visited(graph.size(), -1);
  queue<int> q;
  q.push(s);
  visited[s] = s;

  while (!q.empty()) {
    int v = q.front();
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

  return restore_path(visited, s, e);
}

int find_bottleneck(vector<vector<Edge>>& graph, vector<int>& path) {
  int bottleneck = INT32_MAX;
  for (int i = 0; i < path.size() - 1; ++i) {
    for (auto& next : graph[path[i]]) {
      if (next.to == path[i + 1]) {
        bottleneck = min(bottleneck, next.weight);
        break;
      }
    }
  }
  return bottleneck;
}

int update_graph(vector<vector<Edge>>& graph, vector<int>& path) {
  int bottleneck = find_bottleneck(graph, path);

  for (int i = 0; i < path.size() - 1; ++i) {
    for (auto& next : graph[path[i]]) {
      if (next.to == path[i + 1]) {
        next.weight -= bottleneck;
        break;
      }
    }
  }

  for (int i = path.size() - 1; i > 0; --i) {
    for (auto& prev : graph[path[i]]) {
      if (prev.to == path[i - 1]) {
        prev.weight += bottleneck;
        break;
      }
    }
  }

  return bottleneck;
}

bool edge_exists(vector<vector<Edge>>& graph, int s, int e) {
  for (auto& edge : graph[s]) {
    if (edge.to == e) return true;
  }
  return false;
}

vector<vector<Edge>> build_adj_graph(vector<vector<Edge>>& graph) {
  vector<vector<Edge>> adj_graph(graph.size());
  for (int from = 0; from < graph.size(); ++from) {
    for (auto& edge : graph[from]) {
      adj_graph[from].push_back({edge.to, edge.weight});
      if (!edge_exists(graph, edge.to, from)) {
        adj_graph[edge.to].push_back({from, 0});
      }
    }
  }

  return std::move(adj_graph);
}

int max_flow(vector<vector<Edge>>& graph, int s, int e) {
  vector<vector<Edge>> adj_graph = build_adj_graph(graph);
  vector<int> path;
  int flow = 0;
  while (!(path = bfs(adj_graph, s, e)).empty()) {
    flow += update_graph(adj_graph, path);
  }
  return flow;
}

int main() {
  ios_base::sync_with_stdio(false);
  // ifstream cin("input.txt");

  vector<vector<Edge>> graph;
  int n, m;
  // n -- vertices
  // m -- edges
  cin >> n >> m;
  graph = vector<vector<Edge>>(n);

  for (int i = 0; i < m; ++i) {
    int u, v, w;
    cin >> u >> v >> w;

    for (auto& vert : graph[u - 1]) {
      if (vert.to == v - 1) {
        vert.weight += w;
        w = 0;
        break;
      }
    }

    if (w > 0) graph[u - 1].push_back({v - 1, w});
  }

  cout << max_flow(graph, 0, n - 1) << endl;
}
