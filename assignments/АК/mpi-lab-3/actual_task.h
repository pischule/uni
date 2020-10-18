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

    double f1(double y) override {
        return y * y;
    }

    double f2(double y) override {
        return y;
    }

    double f3(double x) override {
        return std::sin(x);
    }

    double f4(double x) override {
        return x;
    }

    double F(double y, double x) override {
        return y * x;
    }

};

#endif //MPI_LAB_3_CLION_ACTUAL_TASK_H
