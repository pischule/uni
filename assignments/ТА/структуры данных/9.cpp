#include <iostream>
#include <fstream>
#include <stack>

int main() {
    std::ifstream fin("input.txt");
    int n;
    fin >> n;
    double x, y;
    int z;
    std::stack<int> st;
    for (int i = 0; i < n; ++i) {
        fin >> x >> y >> z;
        if (!st.empty() && st.top() == z) {
            st.pop();
        } else {
            st.push(z);
        }
    }
    std::ofstream fout("output.txt");
    fout << (st.empty() ? "Yes" : "No" )<< std::endl;
}
