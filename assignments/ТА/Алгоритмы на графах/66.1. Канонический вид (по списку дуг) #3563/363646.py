fin, fout = open('input.txt'), open('output.txt', 'w')
n = int(fin.readline())
p = [0]*n
for i in range(n-1):
    a, b = map(int, fin.readline().split())
    p[b-1] = a
fout.write(' '.join(map(str, p)))
fin.close(), fout.close()
