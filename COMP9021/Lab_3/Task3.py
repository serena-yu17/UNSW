op = dict()
for i in range(32):
    for j in range(32):
        n = i ** 2 + j ** 2
        if n > 100 and n < 999:
            op[n] = (i, j)
for n in sorted(op):
    if n + 1 in op and n + 2 in op:
        print(f"({n}, {n+1}, {n+2}) (equal to ({op[n][0]}^2+{op[n][1]}^2, {op[n+1][0]}^2+{op[n+1][1]}^2, {op[n+2][0]}^2+{op[n+2][1]}^2)) is a solution.")
