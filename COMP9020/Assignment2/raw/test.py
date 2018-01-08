def iter_a(n):
    if n < 2:
        return n
    else:
        x = 1
        y = 0
        i = 1
        while i < n:
            t = x
            x = 5 * x - 6 * y
            y = t
            i += 1
        return x


print("n\t\ta^n\t\ta^n+2^n")
for i in range(100):
    it = iter_a(i)
    print(i, it, it + 2 ** i, sep="\t\t")
