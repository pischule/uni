#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

struct DSU {
    DSU(int n)
        :data(vector<int>(n+1, -1))
    {}

    void add(int x, int y) {
        int x_p = find(x);
        int y_p = find(y);

        if (x_p == -1 && y_p == -1) {
            data[x] = data[y] = y;
        } else if (x_p == -1) { // b != -1
            data[x] = y_p;
        } else if (y_p == -1) { // a != -1
            data[y] = x_p;
        } else {
            data[x_p] = data[y_p];
        }
    }

    int find(int x) {
        if (data[x] == -1) {
            return -1;
        }
        while (data[x] != x) {
            x = data[x];
        }
        return x;
    }

private:
    vector<int> data;
};

int main() {
    int n; // число переменных
    int m; // число строк

    ifstream fin("equal-not-equal.in");
    ofstream fout("equal-not-equal.out");
    ios_base::sync_with_stdio(false);

    fin >> n >> m;

    DSU dsu(n);
    vector< pair<int, int> > not_equals;

    int a, b;
    string s;
    bool correct = true;
    char c;

    for (int i = 0; i < m; ++i) {
        fin >> c >> a >> s >> c >> b;
        if (s == "==") {
            dsu.add(a, b);
        } else {
            if (a == b) {
                correct = false;
                break;
            }
            not_equals.emplace_back(a, b);
        }
    }

    for (pair<int, int> p : not_equals) {
        int da = dsu.find(p.first);
        int db = dsu.find(p.second);
        if (da != -1 && da == db) {
            correct = false;
            break;
        }
    }

    fout << (correct ? "Yes" : "No");
    return 0;
}
