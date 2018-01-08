from math import log10


def print_square(lst):
    size = len(lst)
    maxelem = 0
    for j in range(size):
        for i in range(size):
            if lst[i][j] is not None and lst[i][j] > maxelem:
                maxelem = lst[i][j]
    leng = int(log10(maxelem)) + 1
    for j in range(size):
        for i in range(size):
            if lst[i][j] == 0:
                print(' ' * (leng), '.', sep='', end='')
            else:
                print(' ' * (leng - int(log10(lst[i][j]))), lst[i][j], sep='', end='')
        print()


def is_magic_square(lst):
    leng = len(lst)
    uniform_sum = int((leng ** 2 + 1) * leng / 2)
    for ls in lst:
        if len(ls) != leng:
            return False
    for i in range(leng):
        sumx = 0
        sumy = 0
        for j in range(leng):
            sumx += lst[i][j]
            sumy += lst[j][i]
        if sumx != uniform_sum or sumy != uniform_sum:
            return False
    return True


def bachet_magic_square(n):
    if n & 1 == 0:
        return []
    sq = [None] * (2 * n - 1)
    for i in range(2 * n - 1):
        sq[i] = [0] * (2 * n - 1)
    num = 1
    x0 = n - 1
    y0 = 0
    for i in range(n):
        x = x0
        y = y0
        for j in range(n):
            sq[x][y] = num
            x += 1
            y += 1
            num += 1
        x0 -= 1
        y0 += 1
    # Re-arrange
    for y in range(n // 2):
        for x in range(n - 1 - i, n + i):
            if sq[x][y] != 0:
                sq[x][y + n] = sq[x][y]
                sq[x][y] = 0
            if sq[x][2 * n - 2 - y] != 0:
                sq[x][n - 2 - y] = sq[x][2 * n - 2 - y]
                sq[x][2 * n - 2 - y] = 0
            if sq[y][x] != 0:
                sq[y + n][x] = sq[y][x]
                sq[y][x] = 0
            if sq[2 * n - 2 - y][x] != 0:
                sq[n - 2 - y][x] = sq[2 * n - 2 - y][x]
                sq[2 * n - 2 - y][x] = 0
    output = [None] * n
    for i in range(n):
        output[i] = []
    start = n // 2
    for j in range(start, start + n):
        for i in range(start, start + n):
            output[i - start].append(sq[i][j])
    return output


def siamese_magic_square(n):
    if n & 1 == 0:
        return []
    sq = [None] * n
    for i in range(n):
        sq[i] = [0] * n
    x = n // 2
    y = 0
    for num in range(1, n ** 2 + 1):
        sq[x][y] = num
        x += 1
        y -= 1
        if x == n:
            x = 0
        if y == -1:
            y = n - 1
        if x == n and y == 0:
            y -= 1
        if sq[x][y] != 0:
            x -= 1
            y += 2
            if x == -1:
                x = n - 1
            if y == n:
                y = 0
            elif y == n + 1:
                y = 1
    return sq


#
# 0 = L, 1 = U, 2 = X
def lux_magic_square(n):
    if (n - 2) % 4 != 0:
        return []
    k = (n - 2) // 4
    sq = [None] * n
    for i in range(n):
        sq[i] = [0] * n
    lux = [None] * (2 * k + 1)
    for i in range(2 * k + 1):
        lux[i] = [None] * (2 * k + 1)
    for j in range(k + 1):
        for i in range(2 * k + 1):
            lux[i][j] = 0
    for i in range(2 * k + 1):
        lux[i][k + 1] = 1
    for j in range(k + 2, 2 * k + 1):
        for i in range(2 * k + 1):
            lux[i][j] = 2
    lux[k][k + 1] = 0
    lux[k][k] = 1
    x = k
    y = 0
    for i in range(0, n ** 2, 4):
        if lux[x][y] == 0:
            sq[x * 2][y * 2] = i + 4
            sq[x * 2 + 1][y * 2] = i + 1
            sq[x * 2][y * 2 + 1] = i + 2
            sq[x * 2 + 1][y * 2 + 1] = i + 3
        elif lux[x][y] == 1:
            sq[x * 2][y * 2] = i + 1
            sq[x * 2 + 1][y * 2] = i + 4
            sq[x * 2][y * 2 + 1] = i + 2
            sq[x * 2 + 1][y * 2 + 1] = i + 3
        elif lux[x][y] == 2:
            sq[x * 2][y * 2] = i + 1
            sq[x * 2 + 1][y * 2] = i + 4
            sq[x * 2][y * 2 + 1] = i + 3
            sq[x * 2 + 1][y * 2 + 1] = i + 2
        x += 1
        y -= 1
        if x == 2 * k + 1:
            x = 0
        if y == -1:
            y = 2 * k
        if sq[x * 2][y * 2] != 0:
            x -= 1
            y += 2
            if x == -1:
                x = 2 * k
            if y == 2 * k + 1:
                y = 0
            elif y == 2 * k + 2:
                y = 1
    return sq


if __name__ == "__main__":
    print("Bachet magic square:")
    print_square(bachet_magic_square(7))
    print("\nSiamese magic square:")
    print_square(siamese_magic_square(7))
    print("\nLUX magic square:")
    print_square(lux_magic_square(10))
