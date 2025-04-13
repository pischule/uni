#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <vector>

using namespace std;

int n, m, k;
// n -- число строк
// m -- число столбцов

using point = pair<int, int>;

int operator<(point e1, point e2) {
  if (e1.first != e2.first) {
    return e1.first - e2.first;
  } else {
    return e1.second - e2.second;
  }
}

int shifts[][2] = {{1, 2}, {1, -2}, {-1, 2}, {-1, -2},
                   {2, 1}, {2, -1}, {-2, 1}, {-2, -1}};

set<point> bfs_export_component(set<point>& points) {
  set<point> component;
  if (points.empty()) return component;
  queue<point> q;
  q.push(*points.begin());

  point p = q.front();
  component.emplace(q.front());
  points.erase(q.front());

  while (!q.empty()) {
    point p = q.front();
    q.pop();

    for (auto s : shifts) {
      point new_point{p.first + s[0], p.second + s[1]};
      if (points.count(new_point)) {
        points.erase(new_point);
        component.emplace(new_point);
        q.push(new_point);
      }
    }
  }
  return component;
}

int upper_bound(set<point> free) {
  int count = 0;
  while (!free.empty()) {
    pair<int, int> k = *free.begin();

    int before = free.size();
    free.erase(k);
    for (auto s : shifts) {
      free.erase({k.first + s[0], k.second + s[1]});
    }

    if (before != free.size()) {
      ++count;
    }
  }
  return count;
}

int record;
vector<set<point>> min_coverage_sets;

vector<set<point>> divide_on_components(set<point> points) {
  vector<set<point>> components;
  set<point> s;
  while (!(s = bfs_export_component(points)).empty()) {
    components.push_back(s);
  }
  return components;
}

void dfs(set<point> history, point pos, set<point> free, set<point> knights) {
  int step = history.size();
  if (step > record) return;

  int y = pos.first;
  int x = pos.second;
  int before = free.size();

  knights.erase({pos.first, pos.second});
  history.emplace(pos);

  for (auto s : shifts) free.erase({y + s[0], x + s[1]});
  free.erase({y, x});
  if (before == free.size()) return;

  if (free.empty()) {
    if (step < record) {
      // cout << record << endl;
      record = step;
      min_coverage_sets.clear();
    }
    min_coverage_sets.push_back(history);
    // cout << "step: " << step << "\trecord: " << record << '\t' << pos <<
    // endl;
  } else {
    while (!knights.empty()) {
      dfs(history, *knights.begin(), free, knights);
      knights.erase(*knights.begin());
    }
  }
}

vector<set<point>> min_coverage(set<point> points) {
  record = upper_bound(points);
  min_coverage_sets.clear();
  set<point> free = points;

  while (!points.empty()) {
    dfs(set<point>(), *points.begin(), free, points);
    points.erase(*points.begin());
  }
  return min_coverage_sets;
}

vector<vector<set<point>>> components_min_coverages(set<point> points) {
  vector<vector<set<point>>> components_min_coverage_;

  vector<set<point>> components = divide_on_components(points);
  for (auto& c : components) {
    components_min_coverage_.push_back(min_coverage(c));
  }
  return components_min_coverage_;
}

bool add_one(vector<int>& number, vector<int>& bases) {
  ++number[0];
  for (int i = 0; i < number.size(); ++i) {
    if (number[i] < bases[i]) break;
    number[i] = 0;
    if (i == (number.size() - 1)) return true;
    number[i + 1] += 1;
  }
  return false;
}

void print_matrix_to_file(vector<int> indices, vector<vector<int>> field,
                          ostream& os, vector<vector<set<point>>>& cmcs) {
  for (int i = 0; i < cmcs.size(); ++i) {
    auto& set_of_points = cmcs[i][indices[i]];
    for (auto& p : set_of_points) {
      field[p.first][p.second] = 1;
    }
  }

  for (int i = 0; i < field[0].size(); ++i) {
    for (int j = 0; j < field.size(); ++j) {
      os << field[j][i];
    }
    os << '\n';
  }
  os << '\n';
}

void print_components_coverage(vector<vector<set<point>>>& cmcs,
                               vector<vector<int>>& field) {
  ofstream fout("output.txt");

  vector<int> sizes;
  vector<int> number(cmcs.size(), 0);
  int total_size = 1;
  for (auto& cmc : cmcs) {
    sizes.push_back(cmc.size());
    total_size *= cmc.size();
  }

  fout << total_size << "\n\n";

  for (int i = 0; i < total_size; ++i) {
    print_matrix_to_file(number, field, fout, cmcs);
    if (!number.empty()) add_one(number, sizes);
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  ifstream fin("input.txt");

  fin >> m >> n >> k;
  vector<vector<int>> field(n, vector<int>(m, 0));

  for (int i = 0; i < k; ++i) {
    int x, y;
    fin >> x >> y;
    field[y - 1][x - 1] = 2;
  }

  set<point> points;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      if (!field[i][j]) points.emplace(i, j);
    }
  }

  auto cmcs = components_min_coverages(points);
  print_components_coverage(cmcs, field);

  return 0;
}