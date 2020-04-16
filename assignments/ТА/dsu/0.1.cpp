#include <iostream>
#include <fstream>
#include <vector>

using namespace std;


struct DSU {
    vector<int> data;
    vector<int> size;
    int comp_count;

    DSU(int n)
        :data(n+1), comp_count(n), size(n+1, 1)
    {
        for (int i = 0; i < n+1; ++i) {
            data[i] = i;
        }
    }

    int find(int x) {
        int res = data[x];
        while (res != data[res])
            res = data[res];
        return res;
    }

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
    ifstream fin("input.txt");
    ofstream fout("output.txt");

    int n, q; // количество городов и запросов
    int u, v; // from city, to city
    fin >> n >> q;

    DSU dsu(n);
    for (int i = 0; i < q; ++i) {
        fin >> u >> v;
        dsu.unite(u, v);
        fout << dsu.comp_count << '\n';
    }

    return 0;
}
