#include <iostream>
#include <vector>
#include <string>
#include <fstream>

// tree

using namespace std;

vector<long long> a;
vector<long long> t;
int n;

void build(int v = 1, int l = 0, int r=n) {
    if (r - l == 1)
        t[v] = a[l];
    else {
        int m = (l + r) / 2;
        build(2*v, l, m);
        build(2*v+1, m, r);
        t[v] = t[2*v] + t[2*v+1];
    }
}

void add(int i, int x, int v = 1, int l=0, int r=n ) {
    if (r - l == 1) {
        t[v] += x;
        return;
    }
    int m = (l + r) / 2;
    if (i < m) {
        add(i, x, 2*v, l, m);
    } else {
        add(i, x, 2*v+1, m, r);
    }
    t[v] = t[2*v] + t[2*v+1];
}

long long sum(int l, int r, int v=1, int tl=0, int tr=n) {
    if (l == tl && r == tr) {
        return t[v];
    }
    int m = (tl + tr) / 2;
    if (r <= m) {
        return sum(l, r, 2*v, tl, m);
    } else if (m <= l) {
        return sum(l, r, 2*v+1, m, tr);
    } else {
        return sum(l, m, 2*v, tl, m) + sum(m, r, 2*v+1, m, tr);
    }
}



int main() {
    ios_base::sync_with_stdio(false);
    // ifstream cin("input.txt");

    string tmp_str;
    int tmp_a, tmp_b;
    int q; // number of queries

    cin >> n;
    a = vector<long long>(n);
    t = vector<long long>(4*n);

    for (int i = 0; i < n; ++i)
        cin >> a[i];
    build();

    cin >> q;

    for (int i = 0; i < q; ++i) {
        cin >> tmp_str >> tmp_a >> tmp_b;
        if (tmp_str[0]=='F')
            cout << sum(tmp_a, tmp_b) << '\n';
        else
            add(tmp_a, tmp_b);
    }
    
    return 0;
}
