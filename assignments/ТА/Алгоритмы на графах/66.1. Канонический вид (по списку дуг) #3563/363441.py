f = open("input.txt")
n = int(f.readline())
vertices = [0] * n
for i in range(n-1):
    root, leaf = map(int, f.readline().split())
    vertices[leaf-1] = root
f.close()

f = open("output.txt", "w")
f.write(' '.join(map(str, vertices)))
f.close()
