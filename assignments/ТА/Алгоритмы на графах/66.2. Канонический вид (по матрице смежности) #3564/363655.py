fin, fout = open('input.txt'), open('output.txt', 'w')
n = int(fin.readline())
p = [0]*n
for i in range(n):
    row = map(int, fin.readline().split())
    for j, val in enumerate(row):
        if val:
            p[j] = i+1
fout.write(' '.join(map(str, p)))
fin.close(), fout.close()
