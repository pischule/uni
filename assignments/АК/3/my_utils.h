//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_MY_UTILS_H
#define MPI_LAB_3_CLION_MY_UTILS_H

#include <vector>
#include <iostream>
#include <iomanip>
#include <cmath>

void print(std::vector<double> &a) {
    int k = (int) sqrt(a.size());
    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            std::cout << std::setw(7) << std::setprecision(2) << a[i * k + j];
        }
        std::cout << '\n';
    }
}

#endif //MPI_LAB_3_CLION_MY_UTILS_H
