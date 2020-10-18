## test.sh output
```
+ cd ./cmake-build-debug/
+ mpirun --oversubscribe -np 1 mpi_lab_3_clion -e 0.000001 -n 130 -nv
5.47955
+ mpirun --oversubscribe -np 2 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
2.6535
+ mpirun --oversubscribe -np 2 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 1 -n 130 -nv
4.69454
+ mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
2.97367
+ mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 2 -n 130 -nv
4.88347
+ mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.000001 -1d -n 130 -nv
3.2214
+ mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.000001 -2d -r 2 -c 4 -n 130 -nv
5.79381
```

## results


-np | 1D MPI| 2D MPI| no MPI
----|----|---|---
1|--|--|5.47955
2|2.6535|4.69454| --
4|2.97367|4.88347| --
8|3.2214|5.79381| --