#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> matrix;
vector<int> vertices;
int n;
int current_number;

void dfs(int index) {
  vertices[index] = current_number;
  for (int i = 0; i < n; ++i) {
    if (matrix[index][i] && vertices[i] == 0) {
      ++current_number;
      dfs(i);
    }
  }
}

int main() {
  ifstream fin("input.txt");
  ofstream fout("output.txt");

  fin >> n;

  matrix = vector<vector<int>>(n, vector<int>(n));
  vertices = vector<int>(n);

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      fin >> matrix[i][j];
    }
  }

  current_number = 1;
  for (int i = 0; i < n; ++i) {
    if (!vertices[i]) {
      dfs(i);
      ++current_number;
    }
  }

  for (int i : vertices) fout << i << ' ';
  fout << endl;

  return 0;
}
