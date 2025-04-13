cmake_minimum_required(VERSION 3.6)
project(lab12)

set(CMAKE_CXX_STANDARD 11)
set(WIN_SOCK wsock32 ws2_32)

# task1
add_executable(test_client test_client.cpp)
add_executable(test_server test_server.cpp)
target_link_libraries(test_client ${WIN_SOCK})
target_link_libraries(test_server ${WIN_SOCK})

add_executable(chat_client chat_client.cpp)
add_executable(chat_server chat_server.cpp)
target_link_libraries(chat_client ${WIN_SOCK})
target_link_libraries(chat_server ${WIN_SOCK})

# # task3
# add_executable(tcp-client client.cpp)
# target_link_libraries(tcp-client ${WIN_SOCK})

# add_executable(tcp-server server.cpp)
# target_link_libraries(tcp-server ${WIN_SOCK})