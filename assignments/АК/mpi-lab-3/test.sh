#!/usr/bin/env bash

cd ./cmake-build-debug/

mpirun --oversubscribe -np 1 mpi_lab_3_clion -e 0.000001 -n 130 -nv

mpirun --oversubscribe -np 2 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
mpirun --oversubscribe -np 2 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 1 -n 130 -nv

mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 2 -n 130 -nv

mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 4 -n 130 -nv