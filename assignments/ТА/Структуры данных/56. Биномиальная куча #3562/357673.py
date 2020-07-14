import math

with open('input.txt') as f:
    n = int(f.readline())

a = []
mask = 1
index = 0
while mask <= n:
    if n & mask:
        a.append(index)
    mask = mask << 1
    index += 1

with open('output.txt', 'w') as f:
    f.write('\n'.join(map(str, a)))