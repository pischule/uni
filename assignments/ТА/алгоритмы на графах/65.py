fin, fout = open('input.txt'), open('output.txt', 'w')
n, m = map(int, fin.readline().split())
adj_list = [[] for i in range(n)]
for i in range(m):
    a, b = map(int, fin.readline().split())
    adj_list[a-1].append(b)
    adj_list[b-1].append(a)
for row in adj_list:
    fout.write(str(len(row)) + ' ' + ' '.join(map(str, row)) + '\n')
fin.close(), fout.close()
