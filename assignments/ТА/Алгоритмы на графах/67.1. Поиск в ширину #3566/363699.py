from collections import deque

def bfs(matrix, start, visited, num):
    q = deque()
    q.append(start)
    while q:
        curr = q.popleft()
        if not visited[curr]:
            visited[curr] = num
            num += 1
        for i, v in enumerate(matrix[curr]):
            if v and not visited[i]:
                q.append(i)
    return num
        

fin, fout = open('input.txt'), open('output.txt', 'w')
n = int(fin.readline())
matrix = [list(map(int, fin.readline().split())) for i in range(n)]
visited = [0]*n
num = 1

for i, v in enumerate(visited):
    if not v:
        num = bfs(matrix, i, visited, num)
fout.write(' '.join(map(str, visited)))
fin.close(), fin.close()
