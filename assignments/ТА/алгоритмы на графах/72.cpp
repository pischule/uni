#include <iostream>
#include <vector>
#include <fstream>
#include <queue>
#include <algorithm>

using namespace std;

struct edge {
    int to;
    int dist;
};

struct qd { // queue data
    int from_i;
    int from_c;
    long long dist;
    int to;
};

struct qd_comp {
    bool operator()(const qd &a, const qd &b) {
        return a.dist > b.dist;
    }
};

struct path_with_length {
    vector<int> path;
    long long length;
};


int n, m;
vector<vector<edge>> adj_lst;

path_with_length dijkstra(int start, int end, int k) {
    priority_queue<qd, vector<qd>, qd_comp> q;
    q.push({-1, 0, 0, start});
    vector<vector<qd>> distances(n);
    for (auto& v: distances)
        v.reserve(k);

    qd curr;
    int vc;
    long long alt_dist;
    while (!q.empty() && distances[end].size() < k) {
        curr = q.top();
        q.pop();
        vc = distances[curr.to].size();
        if (vc >= k)
            continue;
        distances[curr.to].push_back(curr);
        for (edge& e: adj_lst[curr.to]) {
            alt_dist = curr.dist + e.dist;
            if (distances[e.to].size() < k)
                q.push({curr.to, vc, alt_dist, e.to});
        }
    }

    vector<int> path;
    long long dist = distances[end][k-1].dist;
    curr = distances[end][k-1];
    while (curr.from_i != -1) {
        path.push_back(curr.to);
        curr = distances[curr.from_i][curr.from_c];
    }
    path.push_back(start);
    reverse(path.begin(), path.end());
    return {path, dist};
}


int main() {
    ios_base::sync_with_stdio(false);
    ifstream fin("input.txt");
    ofstream fout("output.txt");

    fin >> n >> m;
    adj_lst = vector<vector<edge>>(n);
    for (int i = 0; i < m; ++i) {
        int from, to, dist;
        fin >> from >> to >> dist;
        adj_lst[from-1].push_back({to-1, dist});
        adj_lst[to-1].push_back({from-1, dist});
    }
//    int start, end;
//    fin >> start >> end;

    path_with_length pwl = dijkstra(0, n-1, 1);
    fout << pwl.length << '\n';
//    for (int i: pwl.path)
//        fout << i+1 << ' ';

    return 0;
}
