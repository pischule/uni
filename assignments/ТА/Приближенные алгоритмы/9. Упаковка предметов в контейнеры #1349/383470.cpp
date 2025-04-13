#include <exception>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Item {
  Item(int mass, int volume) : m(mass), v(volume) {}
  int m, v;
};

struct Container {
  vector<Item> items;
  int vcap, mcap;

  Container() : vcap(100), mcap(100) {}

  bool can_fit(Item i) { return i.m <= mcap && i.v <= vcap; }

  void add(Item i) {
    vcap -= i.v;
    mcap -= i.m;
    items.emplace_back(i.m, i.v);
  }
};

void algo(vector<Item> &items) {
  ofstream fout("output.txt");

  auto comp = [](Container &a, Container &b) {
    return a.mcap * a.vcap < b.mcap * b.vcap;
  };
  priority_queue<Container, vector<Container>, decltype(comp)> pq(comp);

  Container c;

  pq.push(c);

  for (Item i : items) {
    c = pq.top();
    if (c.can_fit(i)) {
      pq.pop();

    } else {
      c = Container();
    }

    c.add(i);
    pq.push(c);
  }

  fout << pq.size() << '\n';
  while (!pq.empty()) {
    c = pq.top();
    pq.pop();
    for (auto i : c.items) {
      fout << i.m << ", " << i.v << "; ";
    }
    fout << '\n';
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);

  ifstream fin("input.txt");

  vector<Item> items;

  int n;
  fin >> n;
  for (int i = 0; i < n; ++i) {
    int m, v;
    fin >> m >> v;
    if (m * v == 0) {
      return 0;
    }
    items.emplace_back(m, v);
  }

  algo(items);

  return 0;
}