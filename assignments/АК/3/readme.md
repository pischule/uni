# Warning

1. Где-то определенно есть баг:
![оранжевый -- точное, синий -- приближенное](https://user-images.githubusercontent.com/41614960/96636080-730ece80-1325-11eb-8602-32bab5eb5032.png)

2. Неверно выполняются итерации:

**У меня**:

```
0|0|0
0|0|0
0|0|0

1|1|1
1|1|1
1|1|1

2|2|2
2|2|2
2|2|2
```
...

**Должно быть:**

```
0| |0
 | |
0| |0

1|0|1
0| |0
1|0|1

2|1|2
1|0|1
2|1|2
```
...

# Результаты тестирования

## test.sh output
```
+ cd ./cmake-build-debug/
+ EPS=0.00001
+ N=202
+ mpirun -np 1 mpi_lab_3_clion -e 0.00001 -n 202 -nv
21.8566
+ mpirun -np 1 mpi_lab_3_clion -e 0.00001 -1d -n 202 -nv
22.3501
+ mpirun -np 1 mpi_lab_3_clion -e 0.00001 -2d -r 1 -c 1 -n 202 -nv
23.2715
+ mpirun -np 2 mpi_lab_3_clion -e 0.00001 -1d -n 202 -nv
11.3956
+ mpirun -np 2 mpi_lab_3_clion -e 0.00001 -2d -r 2 -c 1 -n 202 -nv
11.9606
+ mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.00001 -1d -n 202 -nv
9.53355
+ mpirun --oversubscribe -np 4 mpi_lab_3_clion -e 0.00001 -2d -r 2 -c 2 -n 202 -nv
9.2313
+ mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.00001 -1d -n 202 -nv
11.1804
+ mpirun --oversubscribe -np 8 mpi_lab_3_clion -e 0.00001 -2d -r 2 -c 4 -n 202 -nv
11.9872

```

## Execution time


-np | 1D MPI| 2D MPI| no MPI
----|----|---|---
1|22.3501|23.2715|21.8566
2|11.3956|11.9606| --
4|9.53355|9.2313| --
8|11.1804|11.9872| --

# Точное решение в Wolfram Mathematica

```mathematica
a = 1; b = 1;
solution = 
 NDSolveValue[{D[u[x, y], {x, 2}] + D[u[x, y], {y, 2}] == x y,
   u[0, y] == y^2,
   u[a, y] == y,
   u[x, 0] == Sin[x],
   u[x, b] == x
   },
   u,
  {x, 0, a}, 
  {y, 0, b} ];

  plot = Plot3D[solution[x, y], {x, 0, a}, {y, 0, b}]
```