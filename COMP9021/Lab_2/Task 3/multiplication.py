def dig(num):
    if num == 0:
        return [0, 0, 0, 0]
    dig_lst = [0] * 4
    i = 3
    while num > 0 and i >= 0:
        dig_lst[i] = num % 10
        num = num // 10
        i -= 1
    return dig_lst


def last(lst, i):
    return int(lst[len(lst) - 1 - i])


if __name__ == "__main__":
    for i in range(100, 1000):
        for j in range(10, 100):
            res3 = i * j
            if res3 >= 10000:
                continue
            digi = dig(i)
            digj = dig(j)
            res1 = i * last(digj, 0)
            res1 = dig(res1)
            res2 = 10 * i * last(digj, 1)
            res2 = dig(res2)
            res3l = dig(res3)
            col = [0] * 4
            for k in range(4):
                col[k] = int(digi[k]) + int(digj[k]) + int(res1[k]) + int(res2[k]) + int(res3l[k])
            if col[0] == col[1] and col[0] == col[2] and col[0] == col[3]:
                print(i, " * ", j, " = ", res3, ", all columns adding up to ", col[0])
