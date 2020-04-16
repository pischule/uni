#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n, 0);
    vector<int> cache(n, 0);

    vector<int> indices(n, -1);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    for (int i = 0; i < n; ++i) {
         cache[i] = 1;
        for (int j = 0; j < i; ++j) {
            if (arr[j] != 0 && arr[i] % arr[j] == 0) {
                if (cache[i] < cache[j] + 1) {
                    cache[i] = cache[j] + 1;
                    indices[i] = j;
                }
            }
        }
    }

    int m = cache[0];
    int mi = 0;
    for (int i = 0; i < n; ++i) {
        if (cache[i] > m) {
            m = cache[i];
            mi = i;
        }
    }

    cout << m << endl;

    vector<int> track;
    while (mi != -1) {
        track.push_back(mi);
        mi = indices[mi];
    }

    for (int i = track.size()-1; i >= 0; --i) {
        cout << track[i] + 1 << ' ';
    }
    return 0;
}
