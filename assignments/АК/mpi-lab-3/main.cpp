#include <iostream>

#include <mpi/mpi.h>

#include "actual_task.h"
#include "my_utils.h"
#include "solvers/one_thread_solver.h"
#include "solvers/one_d_solver.h"
#include "solvers/two_d_solver.h"

enum Mode {
    kSingle = 0,
    k1d = 1,
    k2d = 2
};


int main(int argc, char **argv) {
    MPI_Init(nullptr, nullptr);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // program options
    Mode mode = kSingle;
    bool verbose = true;
    bool show_time = true;
    double eps = 0.00001;
    int n = 12;
    int cols = 1;
    int rows = 2;

    // parse cli args
    int i = 1;
    while (i < argc) {
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
        else if (arg == "-r")
            rows = atoi(argv[++i]);
        else if (arg == "-c")
            cols = atoi(argv[++i]);
        else {
            if (world_rank == 0) {
                cout << ("Options: \n"
                         "-1d                   Use 1d composition\n"
                         "-2d                   Use 2d composition\n"
                         "-v --verbose          Print result\n"
                         "-nv --no-verbose      Don't print result\n"
                         "-t --time             Show execution time\n"
                         "-nt --no-time         Don't show execution time\n"
                         "-e --eps <arg>        Specify accuracy\n"
                         "-n <arg>              Specify number of blocks\n"
                         "-r <arg>              Specify number of rows (for 2d)\n"
                         "-c <arg>              Specify number of rows (for 2d)\n")
                     << endl;
            }

            MPI_Finalize();
            return 0;
        }
        ++i;
    }


    vector<double> result;
    double time_start;
    if (world_rank == 0)
        time_start = MPI_Wtime();

    ActualTask task(n, eps);
    switch (mode) {
        case kSingle:
            result = OneThreadSolver().solve(task);
            break;
        case k1d:
            result = OneDSolver().solve(task);
            break;
        case k2d:
            result = TwoDSolver(rows, cols).solve(task);
            break;
    }

    if (world_rank == 0 && verbose) {
        print(result);
        cout << endl;
    }

    if (world_rank == 0 && show_time) {
        cout << MPI_Wtime() - time_start << endl;
    }

    MPI_Finalize();
    return 0;
}
