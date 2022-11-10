#include "mpi.h"
#include <iostream>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;

int n = 10; // default matrix size
bool verbose = false;
bool generate = false;

// mpirun --oversubscribe -np 4 ./mpi-lab-2 -g <<< '1000'

// $ mpirun --oversubscribe -np 1 ./mpi-lab-2 -g <<< '1000'
// Time: 12.1779
// $ mpirun --oversubscribe -np 2 ./mpi-lab-2 -g <<< '1000'
// Time: 8.66217
// $ mpirun --oversubscribe -np 4 ./mpi-lab-2 -g <<< '1000'
// Time: 11.6641

// $ mpirun --oversubscribe -np 1 ./mpi-lab-2 < ../input.txt 
// Time: 0.0169708
// $ mpirun --oversubscribe -np 2 ./mpi-lab-2 < ../input.txt 
// Time: 0.0156026
// $ mpirun --oversubscribe -np 4 ./mpi-lab-2 < ../input.txt 
// Time: 0.0123719
// $ mpirun --oversubscribe -np 10 ./mpi-lab-2 < ../input.txt 
// Time: 0.0344995

void read_matrix_from_stdin(vector<double> matrix)
{
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> matrix[i*2*n + j];
        }
    }
}

void fill_random_matrix(vector<double> &matrix)
{
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            matrix[i*2*n + j] = rand() % 100 + 1;
        }
    }
}

void init_system(vector<double> &matrix)
{
    matrix = vector<double>(2 * n * n);
    for (int i = 0; i < n; ++i)
    {
        for (int j = n; j < 2 * n; ++j)
        {
            matrix[i * 2 * n + j] = (i == j - n);
        }
    }
}

void print_system(vector<double> &matrix)
{
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < 2 * n; ++j)
        {
            cout << setw(7) << setprecision(2) << matrix[i * 2 * n + j] << ' ';
        }
        cout << '\n';
    }
}

int main(int argc, char *argv[])
{

    MPI_Init(NULL, NULL);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    //parse arguments
    for (int i = 0; i < argc; ++i)
    {
        string arg(argv[i]);
        if (arg == "-v" || arg == "--verbose")
            verbose = true;
        if (arg == "-g" || arg == "--generate")
            generate = true;
    }

    // input matrix size
    if (world_rank == 0)
    {
        cin >> n;
    }

    // send matrix size to all processes
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // we'll slice the matrix in lines of line_height height
    int line_height = n / world_size;

    // if matrix size is not dividible by the number of world_size
    // abort the process
    if (n % world_size != 0)
    {
        cerr << "Matrix size should be devisible by the number of world size" << endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    vector<double> matrix;
    if (world_rank == 0)
    {
        init_system(matrix);
        if (generate)
            fill_random_matrix(matrix);
        else
            read_matrix_from_stdin(matrix);
    }

    // print system if user asked to
    if (world_rank == 0 && verbose)
    {
        cout << "Generated matrix: \n";
        print_system(matrix);
    }

    // a timestamp to test performance
    double t = MPI_Wtime();

    // a part of matrix stored by all processes
    vector<double> a(2 * n * line_height);

    // divide line in lines and send to all processes
    MPI_Scatter(matrix.data(), matrix.size() / world_size, MPI_DOUBLE,
                a.data(), a.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // first phase of gaussian elimination
    int line_size = 2 * n; // line size
    vector<double> line(line_size);
    for (int i = 0; i < n; ++i)
    {
        int line_number = i / line_height;
        int chopped_i = i % line_height;
        if (world_rank == line_number)
        {
            double scale = a[chopped_i * line_size + i];
            for (int j = 0; j < line_size; ++j)
            {
                a[chopped_i * line_size + j] /= scale;
            }
            copy(a.begin() + chopped_i * line_size, a.begin() + (chopped_i + 1) * line_size, line.begin());
        }

        // send substitutable line to all processes
        MPI_Bcast(line.data(), line_size, MPI_DOUBLE, line_number, MPI_COMM_WORLD);

        for (int row = i + 1; row < n; ++row)
        {
            if (row / line_height == world_rank)
            {
                int cr = row % line_height;
                double factor = a[cr * line_size + i];
                for (int col = 0; col < line_size; ++col)
                {
                    a[cr * line_size + col] -= factor * line[col];
                }
            }
        }
    }

    // back substitution phase of gaussian method
    for (int i = n - 1; i > 0; --i)
    {
        int ln = i / line_height;
        if (ln == world_rank)
        {
            int ci = i % line_height;
            copy(a.begin() + ci * line_size, a.begin() + (ci + 1) * line_size, line.begin());
        }
        MPI_Bcast(line.data(), line_size, MPI_DOUBLE, ln, MPI_COMM_WORLD);

        for (int row = i - 1; row >= 0; --row)
        {
            if (row / line_height == world_rank)
            {
                int cr = row % line_height;
                double factor = a[cr * line_size + i];
                for (int col = 0; col < line_size; ++col)
                {
                    a[cr * line_size + col] -= factor * line[col];
                }
            }
        }
    }

    // gather parts of matrix from processes to a single one
    MPI_Gather(a.data(), a.size(), MPI_DOUBLE,
               matrix.data(), a.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // print time and result system if user asked
    if (world_rank == 0)
    {
        if (verbose)
        {
            cout << "\nResult system:\n";
            print_system(matrix);
            cout << endl;
        }

        cout << "Time: " << (MPI_Wtime() - t) << endl;
    }

    MPI_Finalize();

    return 0;
}

// void gauss(vector<vector<double>> &a) {
//     // gaussian elimination phase
//     for (int i = 0; i < n; ++i) {
//         double scale = a[i][i];
//         for (int j = 0; j < 2*n; ++j) {
//             a[i][j] /= scale;
//         }

//         for (int row = i+1; row < n; ++row) {
//             double factor = a[row][i];
//             for (int col = 0; col < 2*n; ++col) {
//                 a[row][col] -= factor * a[i][col];
//             }
//         }
//     }

//     // back substitution phase
//     for (int i = n-1; i > 0; --i) {
//         for (int row = i - 1; row >= 0; --row) {
//             double factor = a[row][i];
//             for (int col = 0; col < 2*n; ++col) {
//                 a[row][col] -= factor * a[i][col];
//             }
//         }
//     }
// }