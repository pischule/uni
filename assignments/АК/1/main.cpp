#include <mpi.h>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <iterator>

// for benchmark (Unix specific)
#include <sys/time.h>
typedef unsigned long long timestamp_t;
static timestamp_t
get_timestamp () {
    struct timeval now;
    gettimeofday (&now, NULL);
    return  now.tv_usec + (timestamp_t)now.tv_sec * 1000000;
}

using namespace std;

// number of elements
const int N = 30*1000*1000;

vector<int> merge(const vector<int> &a, const vector<int> &b) {
    vector<int> c;
    c.reserve(a.size() + b.size());

    int i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] < b[j]) {
            c.push_back(a[i++]);
        } else {
            c.push_back(b[j++]);
        }
    }

    if (i == a.size()) {
        while (j < b.size()) c.push_back(b[j++]);
    } else {
        while (i < a.size()) c.push_back(a[i++]);
    }
    return c;
}

// merges vectors of sorted vectors
vector<int> merge_rec(const vector<vector<int>>  &a, int start_index, int end_index) {
    int size = end_index - start_index;

    if (size < 1) {
        return vector<int>();
    } else if (size == 1) {
        return a[start_index];
    } else {
        int half_index = start_index + size/2;
        return merge(merge_rec(a, start_index, half_index),
                     merge_rec(a, half_index, end_index));
    }
}

// generates a random vector
vector<int> random_vector(int size) {
    vector<int> a(size);
    generate(a.begin(), a.end(), []() -> int {return rand() % 1000;});
    return a;
}


int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // array part size
    int part_size = N/world_size;

    MPI_Barrier(MPI_COMM_WORLD);
    if (world_rank==0) {
        // initialize vector
        vector<int> a = random_vector(N);

        // stopwatch start
        timestamp_t t0 = get_timestamp();

        // send parts to processes
        for (int i = 0; i < world_size-1; ++i) {
            MPI_Send(a.data() + i*part_size,part_size, MPI_INT,i+1,0,MPI_COMM_WORLD);
        }

        vector<vector<int>> parts;

        // process part
        parts.emplace_back(a.begin() + (world_size-1)*part_size, a.end());
        sort(parts.back().begin(), parts.back().end());

        // receive parts
        for (int i = 0; i < world_size-1; ++i) {
            parts.emplace_back(part_size);
            MPI_Recv(parts.back().data(), part_size, MPI_INT, i+1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        // merge sorted arrays
        vector<int> result = merge_rec(parts, 0, parts.size());

        // stopwatch end
        timestamp_t t1 = get_timestamp();
        double secs = (t1 - t0) / 1000000.0L;
        cout << "Time: " << secs << endl;

        cout << "is_sorted: " << (is_sorted(result.begin(), result.end())? "Yes" : "No") << endl;
        cout << "size is the same: " << (result.size() == a.size()? "Yes" : "No") << endl;

    } else {
        // receive, process, send back
        vector<int> a(part_size);
        MPI_Recv(a.data(), part_size, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        sort(a.begin(), a.end());
        MPI_Send(a.data(), part_size, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}
