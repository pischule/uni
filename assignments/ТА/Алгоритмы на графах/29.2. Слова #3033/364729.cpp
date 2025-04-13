#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <vector>

using namespace std;

bool check(vector<vector<vector<string>>> &adj_matrix) {
  // check degree
  vector<int> out_degree(26, 0);
  vector<int> in_degree(26, 0);

  for (int i = 0; i < 26; ++i) {
    for (int j = 0; j < 26; ++j) {
      in_degree[j] += adj_matrix[i][j].size();
      out_degree[i] += adj_matrix[i][j].size();
    }
  }

  for (int i = 0; i < 26; ++i) {
    if (in_degree[i] != out_degree[i]) return false;
  }

  // check components
  vector<bool> visited(26, false);
  int vertex = 0;
  while (!out_degree[vertex]) ++vertex;

  // bfs
  queue<int> visit_queue;
  visit_queue.push(vertex);
  while (!visit_queue.empty()) {
    vertex = visit_queue.front();
    visit_queue.pop();
    if (visited[vertex]) continue;
    visited[vertex] = true;
    for (int i = 0; i < 26; ++i) {
      if (!adj_matrix[vertex][i].empty()) {
        visit_queue.push(i);
      }
    }
  }

  // check that we have one and only one component
  for (int i = 0; i < 26; ++i) {
    if (visited[i] != ((bool)out_degree[i])) return false;
  }
  return true;
}

struct so {  // stack_object
  int from;
  int to;
  string word;
};

// danger! damages adj_matrix object
vector<string> find_path(vector<vector<vector<string>>> &adj_matrix) {
  vector<string> path;
  stack<so> s;

  so v;
  bool flag = true;
  for (int i = 0; i < 26 && flag; ++i) {
    for (int j = 0; j < 26 && flag; ++j) {
      if (!adj_matrix[i][j].empty()) {
        v = {i, j, adj_matrix[i][j].back()};
        adj_matrix[i][j].pop_back();
        flag = false;
      }
    }
  }

  s.push(v);

  bool can_exit;
  while (!s.empty()) {
    v = s.top();
    can_exit = false;

    for (int i = 0; i < 26; ++i) {
      if (!adj_matrix[v.to][i].empty()) {
        v = {v.to, i, adj_matrix[v.to][i].back()};
        adj_matrix[v.from][i].pop_back();
        s.push(v);
        can_exit = true;
        break;
      }
    }

    if (!can_exit) {
      path.push_back(v.word);
      s.pop();
    }
  }

  reverse(path.begin(), path.end());
  return path;
}

int main() {
  ios_base::sync_with_stdio(false);
  ifstream fin("input.txt");
  ofstream fout("output.txt");

  vector<vector<vector<string>>> adj_matrix(26, vector<vector<string>>(26));

  int n;
  fin >> n;

  string word;
  for (int i = 0; i < n; ++i) {
    fin >> word;
    adj_matrix[word.front() - 'a'][word.back() - 'a'].push_back(word);
  }

  if (check(adj_matrix)) {
    fout << "Yes\n";
    vector<string> path = find_path(adj_matrix);
    for (string &s : path) {
      fout << s << '\n';
    }
  } else {
    fout << "No\n";
  }

  return 0;
}
