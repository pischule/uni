import math                             # DP with memoization
cache = {-1: -math.inf, 1: -math.inf}   # looks horrible but its only 10 lines!!!
def f(e):
    if e in cache: return cache[e]
    cache[e] = max(f(e - 2), f(e - 3)) + a[e]
    return cache[e]
with open('input.txt') as file: a = list(map(int, file.read().split()))[1:]
cache[0] = a[0]
r = f(len(a)-1)
with open('output.txt', 'w') as file: file.write(str(r if r > 0 else -1) + '\n')
