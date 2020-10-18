//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ONE_D_SOLVER_H
#define MPI_LAB_3_CLION_ONE_D_SOLVER_H

#include <vector>
#include <algorithm>
#include <cmath>

#include "abstract_mpi_solver.h"
#include "../direction.h"
#include "../block.h"

struct OneDSolver : public MPISolver {
    std::vector<double> solve(AbstractTask &t) override {
        int n = t.n;
        double eps = t.eps;

        if ((n - 2) % world_size) {
            std::cerr << "n - 2 should be divisible by th number of processes" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 2);
        }

        double yh = t.b / n;
        double xh = t.a / n;

        int part_y = (n - 2) / world_size + 2;

        Block u(part_y-2, n-2);

        // fill borders
        if (world_rank == 0) {
            for (int i = 0; i < n - 1; ++i) {
                u[0][i] = t.f3(i * xh);
            }
        }
        if (world_rank == world_size - 1) {
            for (int i = 0; i < n - 1; ++i) {
                u[part_y - 1][i] = t.f4(i * xh);
            }
        }
        for (int i = 1; i < part_y - 1; ++i) {
            u[i][0] = t.f1((world_rank * (part_y - 2) + i) * yh);
            u[i][n-1] = t.f2((world_rank * (part_y - 2) + i) * yh);
        }

        double accuracy;
        do {
            accuracy = 0;
            for (int i = 1; i < part_y - 1; ++i) {
                for (int j = 1; j < n - 1; ++j) {
                    double old_u = u[i][j];
                    u[i][j] = .25 * (u[i][j - 1] + u[i][j+1] +
                                          u[i - 1][j] + u[i + 1][j] -
                                          t.F((world_rank * (part_y - 2) + i) * yh, j * xh) * yh * xh);
                    accuracy = std::max(std::abs(u[i][j] - old_u), accuracy);
                }
            }
            MPI_Allreduce(&accuracy, &accuracy, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);

            if (world_rank != 0)
                MPI_Send(&u[0][n + 1], n - 2, MPI_DOUBLE, world_rank - 1, kUp, MPI_COMM_WORLD);
            if (world_rank != world_size - 1)
                MPI_Send(&u[part_y - 2][1], n - 2, MPI_DOUBLE, world_rank + 1, kDown, MPI_COMM_WORLD);
            if (world_rank != 0)
                MPI_Recv(&u[0][1], n - 2, MPI_DOUBLE, world_rank - 1, kDown, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (world_rank != world_size - 1)
                MPI_Recv(&u[part_y - 1][1], n - 2, MPI_DOUBLE, world_rank + 1, kUp, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
            MPI_Barrier(MPI_COMM_WORLD);

        } while (accuracy > eps);

        if (world_size == 1) return u.v;

        std::vector<double> result;
        if (world_rank == 0) {
            result = std::vector<double>(n * n);
        }

        MPI_Gather(&u[0][n], n * (part_y - 2), MPI_DOUBLE, &result[n], n * (part_y - 2), MPI_DOUBLE, 0, MPI_COMM_WORLD);

        if (world_rank == world_size - 1) {
            MPI_Send(&u[0][part_y - 1], n, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
        }

        if (world_rank == 0) {
            copy(u.v.begin(), u.v.begin() + n, result.begin());
            MPI_Recv(&result[n * (n - 1)], n, MPI_DOUBLE, world_size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        return result;
    };
};

#endif //MPI_LAB_3_CLION_ONE_D_SOLVER_H
