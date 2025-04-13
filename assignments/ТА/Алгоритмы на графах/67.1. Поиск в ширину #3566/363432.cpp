#include <deque>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> matrix;
vector<int> visited;
int n;
int current_number;

void bfs(int index) {
  deque<int> to_visit_queue;
  to_visit_queue.push_back(index);
  visited[index] = current_number++;

  while (!to_visit_queue.empty()) {
    for (int i = 0; i < n; ++i) {
      if (matrix[to_visit_queue.front()][i] && visited[i] == 0) {
        to_visit_queue.push_back(i);
        visited[i] = current_number++;
      }
    }
    to_visit_queue.pop_front();
  }
}

int main() {
  ifstream fin("input.txt");
  ofstream fout("output.txt");

  fin >> n;

  matrix = vector<vector<int>>(n, vector<int>(n));
  visited = vector<int>(n);

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      fin >> matrix[i][j];
    }
  }

  current_number = 1;
  for (int i = 0; i < n; ++i) {
    if (!visited[i]) {
      bfs(i);
    }
  }

  for (int i : visited) fout << i << ' ';
  fout << endl;

  return 0;
}
