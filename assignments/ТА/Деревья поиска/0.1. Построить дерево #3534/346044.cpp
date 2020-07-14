#include <fstream>
#include <iostream>

using namespace std;

struct Node {
  Node *l;
  Node *r;
  int v;

  explicit Node(int val) : l(nullptr), r(nullptr), v(val) {}
};

class Tree {
 public:
  Tree() { root = nullptr; }

  ~Tree() {
    if (root) recursive_delete(root);
    delete root;
  }

  void show(ostream &os) {
    if (root) {
      recursive_show(root, os);
    }
  }

  void add(int val) {
    if (!root) {
      root = new Node(val);
    } else {
      recursive_add(val, root);
    }
  }

 private:
  static void recursive_show(Node *node, ostream &os) {
    os << node->v << '\n';
    if (node->l) {
      recursive_show(node->l, os);
    }
    if (node->r) {
      recursive_show(node->r, os);
    }
  }

  static void recursive_add(int val, Node *node) {
    if (val < node->v) {
      if (node->l) {
        recursive_add(val, node->l);
      } else {
        node->l = new Node(val);
      }
    }
    if (node->v < val) {
      if (node->r) {
        recursive_add(val, node->r);
      } else {
        node->r = new Node(val);
      }
    }
  }

  Node *root;

  static void recursive_delete(Node *node) {
    if (node->l) {
      recursive_delete(node->l);
    }
    if (node->r) {
      recursive_delete(node->r);
    }
    node->l = node->r = nullptr;
  }
};

int main() {
  ifstream fin("input.txt");

  Tree t;

  int i;
  while (fin >> i) {
    t.add(i);
  }

  ofstream fout("output.txt");
  t.show(fout);

  return 0;
}
