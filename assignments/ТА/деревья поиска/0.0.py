#!/usr/bin/python3
numbers = set()

with open('input.txt') as f:
    numbers = set(map(int, f.read().split()))

with open('output.txt', 'w') as f:
    f.write(str(sum(numbers)))