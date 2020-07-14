f = open("input.txt", "r")
n, m = map(int, f.readline().split())
matrix = [[0 for col in range(n)] for row in range(n)]

for i in range(m):
    v1, v2 = map(int, f.readline().split())

    matrix[v1-1][v2-1] = 1
    matrix[v2-1][v1-1] = 1
f.close()

f = open("output.txt", "w")
for row in range(n):
    f.write(' '.join(map(str, matrix[row])))
    f.write('\n')
f.close()
