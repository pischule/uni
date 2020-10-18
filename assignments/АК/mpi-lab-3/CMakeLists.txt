cmake_minimum_required(VERSION 3.17)
project(mpi_lab_3_clion)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_C_COMPILER "/usr/bin/mpicc")
set(CMAKE_CXX_COMPILER "/usr/bin/mpic++")
include_directories(/usr/include/mpi/)

add_executable(mpi_lab_3_clion main.cpp my_utils.h abstract_task.h block.h solvers/abstract_solver.h solvers/one_thread_solver.h solvers/abstract_mpi_solver.h solvers/one_d_solver.h solvers/two_d_solver.h actual_task.h direction.h position_transformer.h)