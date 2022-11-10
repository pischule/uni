//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_TWO_D_SOLVER_H
#define MPI_LAB_3_CLION_TWO_D_SOLVER_H

#include <vector>
#include <mpi/mpi.h>

#include "abstract_mpi_solver.h"
#include "../block.h"
#include "../position_transformer.h"
#include "../direction.h"


struct TwoDSolver : public MPISolver {
private:
    int y_blocks;
    int x_blocks;

    int block_pos_y;
    int block_pos_x;

public:
    TwoDSolver(int y_blocks, int x_blocks) : y_blocks(y_blocks), x_blocks(x_blocks) {
        if (y_blocks * x_blocks != world_size) {
            std::cerr << "yBlock*xBlocks should give number of processes" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 3);
        }

        // current block position among other blocks
        block_pos_x = world_rank % x_blocks;
        block_pos_y = world_rank / x_blocks;
    }

    vector<double> solve(AbstractTask &t) override {
        if ((t.n - 2) % y_blocks || (t.n - 2) % x_blocks) {
            std::cerr << "task's n should be dividable by number of blocks" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 2);
        }

        double yh = t.b / t.n;
        double xh = t.a / t.n;

        Block u((t.n - 2) / y_blocks, (t.n - 2) / x_blocks);

        // transforms local cell coords to absolute double
        PositionTransformer pt(yh, xh, block_pos_y, block_pos_x, u.y, u.x);

        // set block borders (only for blocks that lie on border(again))
        if (block_pos_y == 0) {
            for (int i = 1; i < u.x + 1; ++i) {
                u[0][i] = t.f3(pt.x(i)); //u(0, x)
            }
        }
        if (block_pos_y == y_blocks - 1) {
            for (int i = 1; i < u.x + 1; ++i) {
                u[u.y + 1][i] = t.f4(pt.x(i));
            }
        }
        if (block_pos_x == 0) {
            for (int i = 1; i < u.y + 1; ++i) {
                u[i][0] = t.f1(pt.y(i));
            }
        }
        if (block_pos_x == x_blocks - 1) {
            for (int i = 1; i < u.y + 1; ++i) {
                u[i][u.x + 1] = t.f2(pt.y(i));
            }
        }

        // used as temp buffer
        vector<double> helper_col(u.y);

        double accuracy;
        do {
            accuracy = 0;
            for (int i = 1; i < u.y + 1; ++i) {
                for (int j = 1; j < u.x + 1; ++j) {
                    double old_u = u[i][j];
                    u[i][j] = .25 * (u[i][j - 1] + u[i][j + 1] +
                                     u[i - 1][j] + u[i + 1][j] -
                                     t.F(pt.y(i), pt.x(j)) * yh * xh);
                    accuracy = std::max(std::abs(u[i][j] - old_u), accuracy);
                }
            }

            // sync max absolute difference between processes
            MPI_Allreduce(&accuracy, &accuracy, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);

            // send block borders
            if (block_pos_y != 0) {
                MPI_Send(u.row_ptr(1), u.x, MPI_DOUBLE, world_rank - x_blocks, kUp, MPI_COMM_WORLD);
            }
            if (block_pos_y != y_blocks - 1) {
                MPI_Send(u.row_ptr(u.y), u.x, MPI_DOUBLE, world_rank + x_blocks, kDown, MPI_COMM_WORLD);
            }
            if (block_pos_x != 0) {
                MPI_Send(u.get_col(1).data(), u.y, MPI_DOUBLE, world_rank - 1, kLeft, MPI_COMM_WORLD);
            }
            if (block_pos_x != x_blocks - 1) {
                MPI_Send(u.get_col(u.x).data(), u.y, MPI_DOUBLE, world_rank + 1, kRight,
                         MPI_COMM_WORLD);
            }

            // receive block borders
            if (block_pos_y != 0) {
                MPI_Recv(u.row_ptr(0), u.x, MPI_DOUBLE, world_rank - x_blocks, kDown, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
            }
            if (block_pos_y != y_blocks - 1) {
                MPI_Recv(u.row_ptr(u.y + 1), u.x, MPI_DOUBLE, world_rank + x_blocks, kUp, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
            }
            if (block_pos_x != 0) {
                MPI_Recv(helper_col.data(), u.y, MPI_DOUBLE, world_rank - 1, kRight, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
                u.set_col(helper_col, 0);
            }
            if (block_pos_x != x_blocks - 1) {
                MPI_Recv(helper_col.data(), u.y, MPI_DOUBLE, world_rank + 1, kLeft, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
                u.set_col(helper_col, u.x + 1);
            }


        } while (accuracy > t.eps);


        Block result(0, 0);
        if (world_rank == 0) result = Block(t.n - 2, t.n - 2);

        MPI_Barrier(MPI_COMM_WORLD);

        if (world_rank == 0) {
            // copy first block to result
            for (int i = 0; i < u.y + 2; ++i) {
                for (int j = 0; j < u.x + 2; ++j) {
                    result[i][j] = u[i][j];
                }
            }

            // receive blocks from other processes and copy to result
            for (int i = 1; i < world_size; ++i) {
                MPI_Recv(u.v.data(), u.v.size(), MPI_DOUBLE, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

                int offset_x = i % x_blocks;
                int offset_y = i / x_blocks;

                bool y_start = offset_y != 0;
                bool y_end = offset_y != (y_blocks - 1);
                bool x_start = offset_x != 0;
                bool x_end = offset_x != (x_blocks - 1);

                for (int j = y_start; j < u.y + 2 - y_end; ++j) {
                    for (int k = x_start; k < u.x + 2 - x_end; ++k) {
                        result[j + offset_y * u.y][k + offset_x * u.x] = u[j][k];
                    }
                }
            }

        } else {
            // send block to process with rank = 0
            MPI_Send(u.v.data(), u.v.size(), MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
        }

        return result.v;
    }

};

#endif //MPI_LAB_3_CLION_TWO_D_SOLVER_H
