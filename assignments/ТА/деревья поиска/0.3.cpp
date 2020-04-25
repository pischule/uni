#include <iostream>
#include <fstream>
#include <vector>
#include <stack>

using namespace std;

struct Node {
    int value;  // node value
    int left;   // left node index
    int right;  // right node index
    int min;    // min value in subtree
    int max;    // max value in subtree
};

vector<Node> st; // search tree
bool is_st = true;

// fill max/min values in tree
// also check if the tree is search tree
void dfs() {
    vector<bool> visited(st.size(), false);

    stack<int> s;   // visit stack
    Node* n;        // current node
    int i;          // index

    s.push(0);

    while (!s.empty()) {
        i = s.top();
        if (visited[i]) {
            s.pop();

            if (st[i].left > 0) {
                st[i].min = min(st[i].min, st[st[i].left].min);
                st[i].max = max(st[i].max, st[st[i].left].max);
                if (st[st[i].left].max >= st[i].value)
                    is_st = false;
            }
            if (st[i].right > 0) {
                st[i].min = min(st[i].min, st[st[i].right].min);
                st[i].max = max(st[i].max, st[st[i].right].max);
                if (st[i].value > st[st[i].right].min)
                    is_st = false;
            }
            continue;
        }

        n = &st[i];
        
        if (n->right > 0 && !visited[n->right]) {
            s.push(n->right);
        }

        if (n->left > 0 && !visited[n->left]) {
            s.push(n->left);
        }
        
        visited[i] = true;
    }
}


int main() {
    ifstream fin("bst.in");
    ofstream fout("bst.out");

    int n; // number of nodes
    fin >> n;

    st.reserve(n);

    int value, from;
    char direction;

    fin >> value;
    st.push_back({value, -1, -1, value, value});

    // read tree from file
    bool is_tree = true;
    for (int i = 1; i < n; ++i) {
        fin >> value >> from >> direction;
        st.push_back({value, -1, -1, value, value});
        if (direction == 'L') {
            st[from-1].left = i;
        }
        else {
            st[from-1].right = i;
        }
    }

    dfs();
    fout << (is_st ? "YES" : "NO") << endl;

    return 0;
}
