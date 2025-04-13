f = open("input.txt")
n = int(f.readline())

vertices = [0]*n
for root in range(n):
    leafs = f.readline().split()
    for l in range(n):
        if leafs[l] == '1':
            vertices[l] = root+1
f.close()

f = open("output.txt", "w")
f.write(' '.join(map(str, vertices)))
