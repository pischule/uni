from collections import deque

def dfs(matrix, start, visited, num):
    s = deque()
    s.append(start)
    while s:
        curr = s.pop()
        if not visited[curr]:
            visited[curr] = num
            num += 1
        for i in reversed(range(len(matrix[curr]))):
            if matrix[curr][i] and not visited[i]:
                s.append(i)
    return num
        

fin, fout = open('input.txt'), open('output.txt', 'w')
n = int(fin.readline())
matrix = [list(map(int, fin.readline().split())) for i in range(n)]
visited = [0]*n
num = 1

for i, v in enumerate(visited):
    if not v:
        num = dfs(matrix, i, visited, num)
fout.write(' '.join(map(str, visited)))
fin.close(), fin.close()
