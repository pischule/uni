#include <iostream>
#include <vector>

int main() {
    int n, m = 1;
    std::cin >> n;
    std::vector<int> arr(n, 0);
    std::vector<int> cache(n, 1);
    for (int i = 0; i < n; ++i) std::cin >> arr[i];

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < i; ++j)
            if (arr[j] != 0 && arr[i] % arr[j] == 0)
                    cache[i] = std::max(cache[i], cache[j] + 1);
    for (int i = 0; i < n; ++i)
        m = std::max(m, cache[i]);
    std::cout << n - m;
    return 0;
}
