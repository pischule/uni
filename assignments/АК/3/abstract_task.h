//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_ABSTRACT_TASK_H
#define MPI_LAB_3_CLION_ABSTRACT_TASK_H

struct AbstractTask {
    AbstractTask(int a, int b, int n, double eps) : a(a), b(b), n(n), eps(eps) {}

    virtual double f1(double y) = 0;

    virtual double f2(double y) = 0;

    virtual double f3(double x) = 0;

    virtual double f4(double x) = 0;

    virtual double F(double y, double x) = 0;

    double a;
    double b;
    int n;
    double eps;
};

#endif //MPI_LAB_3_CLION_ABSTRACT_TASK_H
