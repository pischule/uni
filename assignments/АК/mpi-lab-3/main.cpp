#include <iostream>
#include <iomanip>
#include <vector>
#include <mpi/mpi.h>
#include <cmath>
#include <limits>
#include <string>
#include <cmath>

// 15 % 3 == 0 => 3 var

using namespace std;

int world_size, world_rank;

// u(x, y)
double f1(double y) { return y * y; }  // u(y, 0)
double f2(double y) { return y; }      // u(y, a)
double f3(double x) { return sin(x); } // u(0, x)
double f4(double x) { return x; }      // u(b, x)
double F(double y, double x) { return x * y; }

enum modes
{
    kSingle = 0,
    k1d = 1,
    k2d = 2
};

// default settings
// default mode
modes mode = kSingle;
// x_max, y_max
double a = 1;
double b = 1;
// accuracy
double eps = 0.00001;
// size of mesh
int n = 10;
// use ouput
bool verbose = true;
// show time
bool show_time = true;

vector<double> solve1thread()
{
    vector<double> u(n * n, 0);
    double x_h = a / n;
    double y_h = b / n;
    for (int i = 0; i < n; ++i)
    {
        u[i * n + 0] = f1(y_h * i);
        u[i * n + n - 1] = f2(y_h * i);
        u[0 * n + i] = f3(x_h * i);
        u[(n - 1) * n + i] = f4(x_h * i);
    }

    double accuracy;
    do
    {
        accuracy = 0;
        for (int i = 1; i < n - 1; ++i)
        {
            for (int j = 1; j < n - 1; ++j)
            {
                double old_u = u[i * n + j];
                u[i * n + j] = .25 * (u[i * n + j - 1] + u[i * n + j + 1] +
                                      u[(i - 1) * n + j] + u[(i + 1) * n + j] - F(i * y_h, j * x_h) * x_h * y_h);
                accuracy = max(abs(u[i * n + j] - old_u), accuracy);
            }
        }
    } while (accuracy > eps);
    return std::move(u);
}

void print(vector<vector<double>> &a)
{
    for (auto &line : a)
    {
        for (auto el : line)
        {
            cout << setw(7) << setprecision(2) << el;
        }
        cout << '\n';
    }
}

void print(vector<double> &a)
{
    int k = (int)sqrt(a.size());
    for (int i = 0; i < k; ++i)
    {
        for (int j = 0; j < k; ++j)
        {
            cout << setw(7) << setprecision(2) << a[i * k + j];
        }
        cout << '\n';
    }
}

vector<double> oneD()
{
    if ((n - 2) % world_size)
    {
        cerr << "n - 2 should be divisible by th number of processes" << endl;
        MPI_Abort(MPI_COMM_WORLD, 2);
    }

    double yh = b / n;
    double xh = a / n;

    int part_y = (n - 2) / world_size + 2;

    vector<double> u(part_y * n, 0);

    // fill borders
    if (world_rank == 0)
    {
        for (int i = 0; i < n; ++i)
        {
            u[i] = f3(i * xh);
        }
    }
    if (world_rank == world_size - 1)
    {
        for (int i = 0; i < n; ++i)
        {
            u[(part_y - 1) * n + i] = f4(i * xh);
        }
    }
    for (int i = 1; i < part_y - 1; ++i)
    {
        u[i * n] = f1((world_rank * (part_y - 2) + i) * yh);
        u[i * n + n - 1] = f2((world_rank * (part_y - 2) + i) * yh);
    }

    double accuracy;
    do
    {
        accuracy = 0;
        for (int i = 1; i < part_y - 1; ++i)
        {
            for (int j = 1; j < n - 1; ++j)
            {
                double old_u = u[i * n + j];
                u[i * n + j] = .25 * (u[i * n + j - 1] + u[i * n + j + 1] +
                                      u[(i - 1) * n + j] + u[(i + 1) * n + j] -
                                      F((world_rank * (part_y - 2) + i) * yh, j * xh) * yh * xh);
                accuracy = max(abs(u[i * n + j] - old_u), accuracy);
            }
        }
        MPI_Allreduce(&accuracy, &accuracy, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);
        if (world_rank != 0)
            MPI_Send(&u[n + 1], n - 2, MPI_DOUBLE, world_rank - 1, 0, MPI_COMM_WORLD);
        if (world_rank != world_size - 1)
            MPI_Send(&u[(part_y - 2) * n + 1], n - 2, MPI_DOUBLE, world_rank + 1, 0, MPI_COMM_WORLD);
        if (world_rank != 0)
            MPI_Recv(&u[1], n - 2, MPI_DOUBLE, world_rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        if (world_rank != world_size - 1)
            MPI_Recv(&u[(part_y - 1) * n + 1], n - 2, MPI_DOUBLE, world_rank + 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Barrier(MPI_COMM_WORLD);

    } while (accuracy > eps);

    vector<double> result;
    if (world_rank == 0)
        result = vector<double>(n * n);
    MPI_Gather(&u[n], n * (part_y - 2), MPI_DOUBLE, &result[n], n * (part_y - 2), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (world_rank == world_size - 1)
        MPI_Send(&u[(part_y - 1) * n], n, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    if (world_rank == 0)
    {
        copy(u.begin(), u.begin() + n, result.begin());
        MPI_Recv(&result[n * (n - 1)], n, MPI_DOUBLE, world_size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    return result;
}

int main(int argc, char **argv)
{
    MPI_Init(NULL, NULL);

    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // parse cli args
    int i = 1;
    while (i < argc)
    {
        string arg(argv[i]);
        if (arg == "-1d")
            mode = k1d;
        else if (arg == "-2d")
            mode = k2d;
        else if (arg == "-v" || arg == "--verbose")
            verbose = true;
        else if (arg == "-nv" || arg == "--no-verbose")
            verbose = false;
        else if (arg == "-t" || arg == "--time")
            show_time = true;
        else if (arg == "-nt" || arg == "--no-time")
            show_time = false;
        else if (arg == "-e" || arg == "--eps")
            eps = atof(argv[++i]);
        else if (arg == "-n")
            n = atoi(argv[++i]);
        else
        {
            if (world_rank == 0)
            {
                cout << ("Options: \n"
                         "-1d                   Use 1d composition\n"
                         "-2d                   Use 2d composition\n"
                         "-v --verbose          Print result\n"
                         "-nv --no-verbos       Don't print result\n"
                         "-t --time             Show execution time\n"
                         "-nt --no-time         Don't show execution time\n"
                         "-e --eps <arg>        Specify accuracy\n"
                         "-n <arg>              Specify number of blocks\n")
                     << endl;
            }

            MPI_Finalize();
            return 0;
        }
        ++i;
    }

    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    vector<double> result;

    double time_start;
    if (world_rank == 0)
        time_start = MPI_Wtime();

    switch (mode)
    {
    case kSingle:
        result = solve1thread();
        break;

    case k1d:
        result = oneD();
        break;
    }

    if (world_rank == 0 && verbose)
    {
        print(result);
    }

    if (world_rank == 0 && show_time)
    {
        cout << endl
             << MPI_Wtime() - time_start << endl;
    }

    MPI_Finalize();

    return 0;
}
