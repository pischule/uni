//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_BLOCK_H
#define MPI_LAB_3_CLION_BLOCK_H

#include <vector>

struct Block {
    // size of actual block(without borders)
    int y;
    int x;

    std::vector<double> v;

    Block(int y, int x)
            : y{y}, x{x} {
        v = std::vector<double>((x + 2) * (y + 2));

    }

    double *operator[](int y) { return &v[y * (x + 2)]; }

    // with (max_y - 2) elements
    std::vector<double> get_col(int x) {
        std::vector<double> col(y);
        for (int i = 1; i < y + 1; ++i) {
            col[i - 1] = (*this)[i][x];
        }
        return move(col);
    }

    // put (max_y - 2) col to v
    void set_col(std::vector<double> &col, int x) {
        for (int i = 1; i < y + 1; ++i) {
            (*this)[i][x] = col[i - 1];
        }
    }

    // starting from x = 1
    double *row_ptr(int y_) {
        return &v[y_ * (x + 2)];
    }
};

#endif //MPI_LAB_3_CLION_BLOCK_H
