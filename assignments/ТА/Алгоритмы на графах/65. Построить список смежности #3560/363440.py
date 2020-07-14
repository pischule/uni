#!/usr/bin/python3

f = open("input.txt")
n, m = map(int, f.readline().split())

vertex_list = [[] for vertex in range(n)]

for i in range(m):
    v1, v2 = map(int, f.readline().split())
    vertex_list[v1 - 1].append(v2)
    vertex_list[v2 - 1].append(v1)
f.close()

f = open("output.txt", "w")

out_string = ""
for vertex in vertex_list:
    out_string += str(len(vertex)) + ' ' + ' '.join(map(str, vertex)) + '\n'

f.write(out_string)
f.close()
