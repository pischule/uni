cmake_minimum_required(VERSION 3.0.0)
project(mpi-lab-1 VERSION 0.1.0)

find_package(MPI REQUIRED)

include_directories(${MPI_INCLUDE_PATH})

add_executable(mpi-lab-1 main.cpp)
target_link_libraries(mpi-lab-1 ${MPI_LIBRARIES})

if(MPI_COMPILE_FLAGS)
  set_target_properties(mpi-lab-1 PROPERTIES
    COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
endif()

if(MPI_LINK_FLAGS)
  set_target_properties(mpi-lab-1 PROPERTIES
    LINK_FLAGS "${MPI_LINK_FLAGS}")
endif()
