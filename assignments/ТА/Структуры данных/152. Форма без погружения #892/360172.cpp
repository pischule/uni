#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

int n, m, i0, j0;
vector<vector<int>> form;
struct Pos {
  int y, x;
};

const vector<Pos> directions{{1, 0}, {0, 1}, {-1, 0}, {0, -1}};

struct Point {
  Pos pos;
  int land_height;
  Point(Pos pos, int land_height) : pos(pos), land_height(land_height) {}

  Point(int y, int x, int land_height) : pos{y, x}, land_height(land_height) {}
};

inline bool operator<(Point a, Point b) {
  return a.land_height > b.land_height;
}

inline bool is_legal(Pos p) {
  return p.x >= 0 && p.y >= 0 && p.y < n && p.x < m;
}

long f() {
  int max_h = INT32_MIN;
  priority_queue<Point> pq;
  vector<vector<bool>> visited(n, vector<bool>(m, false));
  vector<vector<int>> water_on_top(n, vector<int>(m, 0));

  for (int i = 0; i < n; ++i) {
    visited[i][0] = visited[i][m - 1] = true;
    pq.push(Point(i, 0, form[i][0]));
    pq.push(Point(i, m - 1, form[i][m - 1]));
  }

  for (int j = 1; j < m - 1; ++j) {
    visited[0][j] = visited[n - 1][j] = true;
    pq.push(Point(0, j, form[0][j]));
    pq.push(Point(n - 1, j, form[n - 1][j]));
  }

  while (!pq.empty()) {
    Point curr = pq.top();
    pq.pop();
    max_h = max(max_h, curr.land_height);

    for (auto& dir : directions) {
      Pos new_pos{curr.pos.y + dir.y, curr.pos.x + dir.x};
      if (is_legal(new_pos) && !visited[new_pos.y][new_pos.x]) {
        visited[new_pos.y][new_pos.x] = true;
        Point new_point(new_pos, form[new_pos.y][new_pos.x]);
        pq.push(new_point);
        if (new_point.land_height < max_h) {
          water_on_top[new_pos.y][new_pos.x] = max_h - new_point.land_height;
        }
      }
    }
  }

  queue<Pos> down_queue;
  down_queue.push({i0, j0});
  // invert visited/not_visited
  visited[i0][j0] = false;
  while (!down_queue.empty()) {
    Pos curr = down_queue.front();
    down_queue.pop();

    for (Pos dir : directions) {
      Pos n_p{curr.y + dir.y, curr.x + dir.x};
      if (is_legal(n_p) && visited[n_p.y][n_p.x] &&
          (form[curr.y][curr.x] + water_on_top[curr.y][curr.x]) >=
              (form[n_p.y][n_p.x] + water_on_top[n_p.y][n_p.x])) {
        visited[n_p.y][n_p.x] = false;
        down_queue.push(n_p);
      }
    }
  }

  long total_water = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      if (!visited[i][j]) {
        total_water += water_on_top[i][j];
      }
    }
  }
  return total_water;
}

int main() {
  ifstream fin("in.txt");
  ofstream fout("out.txt");

  long volume;

  fin >> n >> m;
  fin >> i0 >> j0 >> volume;
  --i0, --j0;

  form = vector<vector<int>>(n, vector<int>(m));
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      fin >> form[i][j];
    }
  }

  fout << min(volume, f()) << endl;
  return 0;
}