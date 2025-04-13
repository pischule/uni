#include <fstream>
#include <iostream>

using namespace std;

struct Node {
  Node* l;
  Node* r;
  Node* p;  // parent
  int v;

  explicit Node(int val, Node* parent = nullptr)
      : l(nullptr), r(nullptr), p(parent), v(val) {}
};

class Tree {
 public:
  Tree() { root = nullptr; }

  ~Tree() {
    if (root) recursive_free(root);
    delete root;
  }

  void show(ostream& os) {
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
  void replace_child(Node* parent, Node* old, Node* new_node) {
    if (!parent)
      root = new_node;
    else if (parent->l == old)
      parent->l = new_node;
    else if (parent->r == old)
      parent->r = new_node;
  }

 public:
  void del(int value) {
    Node* parent_node = nullptr;
    Node* v = root;

    while (true) {
      if (!v) return;
      if (value < v->v) {
        parent_node = v;
        v = v->l;
      } else if (value > v->v) {
        parent_node = v;
        v = v->r;
      } else {
        break;
      }
    }

    Node* result = nullptr;

    if (!v->l) {
      result = v->r;
    } else if (!v->r) {
      result = v->l;
    } else {
      Node* min_node_parent = v;
      Node* min_node = v->r;
      while (min_node->l) {
        min_node_parent = min_node;
        min_node = min_node->l;
      }
      result = v;
      v->v = min_node->v;
      replace_child(min_node_parent, min_node, min_node->r);
    }
    replace_child(parent_node, v, result);
  }

 private:
  static Node* find_node(Node* root, int val) {
    if (root == nullptr) return nullptr;
    if (root->v == val) return root;
    if (val < root->v)
      return find_node(root->l, val);
    else
      return find_node(root->r, val);
  }

  static Node* recursive_minimum(Node* node) {
    if (node->l == nullptr && node->r == nullptr) {
      return node;
    }
    if (node->l != nullptr) {
      return recursive_minimum(node->l);
    } else {
      return recursive_minimum(node->r);
    }
  }

  static void recursive_show(Node* node, ostream& os) {
    os << node->v << '\n';
    if (node->l) {
      recursive_show(node->l, os);
    }
    if (node->r) {
      recursive_show(node->r, os);
    }
  }

  static void recursive_add(int val, Node* node) {
    if (val < node->v) {
      if (node->l) {
        recursive_add(val, node->l);
      } else {
        node->l = new Node(val, node);
      }
    }
    if (node->v < val) {
      if (node->r) {
        recursive_add(val, node->r);
      } else {
        node->r = new Node(val, node);
      }
    }
  }

  Node* root;

  static void recursive_free(Node* node) {
    if (node->l) {
      recursive_free(node->l);
    }
    if (node->r) {
      recursive_free(node->r);
    }
    node->l = node->r = nullptr;
  }
};

int main() {
  ifstream fin("input.txt");

  int val_to_remove;
  fin >> val_to_remove;

  Tree t;

  int i;
  while (fin >> i) {
    t.add(i);
  }

  t.del(val_to_remove);

  ofstream fout("output.txt");
  t.show(fout);

  return 0;
}
