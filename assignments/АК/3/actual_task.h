//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ACTUAL_TASK_H
#define MPI_LAB_3_CLION_ACTUAL_TASK_H

#include <cmath>
#include "abstract_task.h"

struct ActualTask : public AbstractTask {
    ActualTask(int n, double eps)
            : AbstractTask(1, 1, n, eps) {}


    // u(y, 0)
    double f1(double y) override {
        return y * y;
    }

    // u(y, b)
    double f2(double y) override {
        return y;
    }

    // u(0, x)
    double f3(double x) override {
        return std::sin(x);
    }

    // u(a, x)
    double f4(double x) override {
        return x;
    }

    double F(double y, double x) override {
        return y * x;
    }

};

#endif //MPI_LAB_3_CLION_ACTUAL_TASK_H
