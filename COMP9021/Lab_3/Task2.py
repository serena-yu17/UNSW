from itertools import permutations


def valid(num, row):
    if num < 100000 or num > 999999:
        return 0
    rs = set(row)
    dig = set()
    while num != 0:
        d = num % 10
        if str(d) not in rs:
            return 0
        if d in dig:
            return 0
        else:
            dig.add(d)
            num = num // 10
    return 1


digs = list()
for i in range(10):
    digs.append(chr(i + ord('0')))
perm = permutations(digs, 6)
result = dict()
for row in perm:
    a = int("".join(row[:2]))
    b = int("".join(row[2:4]))
    c = int("".join(row[4:]))
    prod = a * b * c
    if valid(prod, row):
        result[prod] = tuple(sorted([a, b, c]))
for prod in result:
    print("{} x {} x {} = {}".format(result[prod][0], result[prod][1], result[prod][2], prod))
