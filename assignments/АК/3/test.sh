#!/usr/bin/env bash

cd ./cmake-build-debug/

EPS=0.00001
N=202

mpirun -np 1 mpi_lab_3_clion -e $EPS -n $N -nv
mpirun -np 1 mpi_lab_3_clion -e $EPS -1d -n $N -nv
mpirun -np 1 mpi_lab_3_clion -e $EPS -2d -r 1 -c 1 -n $N -nv

mpirun -np 2 mpi_lab_3_clion -e $EPS -1d -n $N -nv
mpirun -np 2 mpi_lab_3_clion -e $EPS -2d -r 2 -c 1 -n $N -nv

mpirun --oversubscribe -np 4 mpi_lab_3_clion -e $EPS -1d -n $N -nv
mpirun --oversubscribe -np 4 mpi_lab_3_clion -e $EPS -2d -r 2 -c 2 -n $N -nv

mpirun --oversubscribe -np 8 mpi_lab_3_clion -e $EPS -1d -n $N -nv
mpirun --oversubscribe -np 8 mpi_lab_3_clion -e $EPS -2d -r 2 -c 4 -n $N -nv
