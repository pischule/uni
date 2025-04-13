def check(arr):
    stack = [0]
    arr_len = len(arr)
    while stack:
        i = stack.pop()
        if i >= arr_len:
            continue
        ai = 2*i+1
        bi = 2*i+2
        if ai < arr_len and arr[i] > arr[ai]:
            return False
        if bi < arr_len and arr[i] > arr[bi]:
            return False
        stack.append(ai)
        stack.append(bi)
    return True


f = open('input.txt')
f.readline()
arr = list(map(int, f.readline().split()))
f.close()

flag = check(arr)

f = open('output.txt', 'w')
f.write("Yes" if flag else "No")
f.close()
