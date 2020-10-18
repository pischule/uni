//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ABSTRACT_MPI_SOLVER_H
#define MPI_LAB_3_CLION_ABSTRACT_MPI_SOLVER_H

#include <mpi/mpi.h>
#include "abstract_solver.h"


struct MPISolver : public AbstractSolver {
    int world_size;
    int world_rank;

    MPISolver() {
        MPI_Comm_size(MPI_COMM_WORLD, &world_size);
        MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    }
};

#endif //MPI_LAB_3_CLION_ABSTRACT_MPI_SOLVER_H
