//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ABSTRACT_SOLVER_H
#define MPI_LAB_3_CLION_ABSTRACT_SOLVER_H

#include <vector>
#include "../abstract_task.h"

struct AbstractSolver {
    virtual std::vector<double> solve(AbstractTask &task) = 0;
};


#endif //MPI_LAB_3_CLION_ABSTRACT_SOLVER_H
