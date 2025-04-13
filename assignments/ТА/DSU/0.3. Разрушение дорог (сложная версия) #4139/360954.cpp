#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

struct DSU {
  vector<int> data;
  vector<int> size;
  int comp_count;

  DSU(int n) : data(n + 1), comp_count(n), size(n + 1, 1) {
    for (int i = 0; i < n + 1; ++i) {
      data[i] = i;
    }
  }

  int find(int x) {
    int res = data[x];
    while (res != data[res]) res = data[res];
    return res;
  }

  void unite(pair<int, int> p) { unite(p.first, p.second); }

  void unite(int to_group, int x) {
    int group_glav = find(to_group);
    int x_glav = find(x);

    if (group_glav != x_glav) {
      --comp_count;
      if (size[group_glav] < size[x_glav]) {
        swap(group_glav, x_glav);
      }
      size[group_glav] += size[x_glav];
    }

    data[x_glav] = group_glav;
  }
};

int main() {
  ios_base::sync_with_stdio(false);

  ifstream fin("input.txt");
  ofstream fout("output.txt");

  int n, m, q;  //города, дороги, землетрясения
  int u, v;
  pair<int, int> p;
  fin >> n >> m >> q;

  DSU dsu(n);

  vector<pair<int, int>> roads;
  roads.reserve(m);
  vector<int> roads_after(m, 0);

  for (int i = 0; i < m; ++i) {
    fin >> u >> v;
    roads.emplace_back(u, v);
    roads_after[i] = 1;
  }

  vector<int> earthquakes;
  int x;
  for (int i = 0; i < q; ++i) {
    fin >> x;
    --x;
    earthquakes.push_back(x);
    roads_after[x] = 0;
  }

  for (int i = 0; i < m; ++i) {
    if (roads_after[i]) {
      dsu.unite(roads[i]);
    }
  }

  vector<int> result;
  result.reserve(q);
  for (int i = q - 1; i >= 0; --i) {
    result.push_back(dsu.comp_count == 1);
    dsu.unite(roads[earthquakes[i]]);
  }

  for (int i = q - 1; i >= 0; --i) {
    fout << result[i];
  }

  fout << endl;

  return 0;
}