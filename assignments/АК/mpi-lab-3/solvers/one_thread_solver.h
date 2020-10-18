//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ONE_THREAD_SOLVER_H
#define MPI_LAB_3_CLION_ONE_THREAD_SOLVER_H

#include <vector>
#include <cmath>
#include "abstract_solver.h"

using namespace std;

struct OneThreadSolver : public AbstractSolver {

    vector<double> solve(AbstractTask &t) override {
        vector<double> u(t.n * t.n, 0);
        double x_h = t.a / t.n;
        double y_h = t.b / t.n;
        for (int i = 1; i < t.n-1; ++i) {
            u[i * t.n + 0] = t.f1(y_h * i);
            u[i * t.n + t.n - 1] = t.f2(y_h * i);
            u[0 * t.n + i] = t.f3(x_h * i);
            u[(t.n - 1) * t.n + i] = t.f4(x_h * i);
        }

        double accuracy;
        do {
            accuracy = 0;
            for (int i = 1; i < t.n - 1; ++i) {
                for (int j = 1; j < t.n - 1; ++j) {
                    double old_u = u[i * t.n + j];
                    u[i * t.n + j] = .25 * (u[i * t.n + j - 1] + u[i * t.n + j + 1] +
                                            u[(i - 1) * t.n + j] + u[(i + 1) * t.n + j]
                                            - t.F(i * y_h, j * x_h) * x_h * y_h);
                    accuracy = max(abs(u[i * t.n + j] - old_u), accuracy);
                }
            }
        } while (accuracy > t.eps);
        return u;
    }
};

#endif //MPI_LAB_3_CLION_ONE_THREAD_SOLVER_H
