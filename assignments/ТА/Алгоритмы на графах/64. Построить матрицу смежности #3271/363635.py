fin, fout = open('input.txt'), open('output.txt', 'w')
n, m = map(int, fin.readline().split())
matrix = [[0]*n for i in range(n)]
for i in range(m):
    a, b = map(int, fin.readline().split())
    matrix[a-1][b-1] = 1
    matrix[b-1][a-1] = 1
fout.write('\n'.join([' '.join(map(str, row)) for row in matrix]))
fin.close(), fout.close()
