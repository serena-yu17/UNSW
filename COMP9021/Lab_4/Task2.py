from math import log10

ub = None
while ub == None:
    ub = input("Enter a non-negative integer: ")
    try:
        ub = int(ub)
    except ValueError:
        print("Invalid value, re-enter.")
    if ub < 0:
        ub = None
        print("Invalid value, re-enter.")
pas = [None] * (ub + 1)
pas[0] = [0] * (ub * 2 + 3)
pas[0][ub + 1] = 1
for row in range(1, ub + 1):
    pas[row] = [0] * (ub * 2 + 3)
    for i in range(ub - row - 1, ub + row + 2):
        pas[row][i] = pas[row - 1][i - 1] + pas[row - 1][i + 1]
        i += 1
largest = pas[ub][ub - (ub & 1) + 1]
leng = int(log10(largest) + 1)

for row in range(0, ub + 1):
    for n in range(ub + row + 2):
        if pas[row][n] == 0:
            print(' ' * leng, end='')
        else:
            space = leng - int(log10(pas[row][n]) + 1)
            print(' ' * space, end='')
            print(pas[row][n], end='')
        n += 1
    print()
