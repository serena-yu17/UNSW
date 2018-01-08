def addition(str1, str2):
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    len1 = len(str1)
    len2 = len(str2)
    lena = len1 + 1
    add = [0] * lena
    ex = 0
    for i in range(len2):
        add[lena - i - 1] = str1[len1 - i - 1] + str2[len2 - i - 1] + ex
        ex = 0
        if add[lena - i - 1] > 9:
            ex = add[lena - i - 1] // 10
            add[lena - i - 1] -= 10
    if len1 > len2:
        for i in range(len1 - len2):
            add[lena - len2 - 1 - i] = str1[len1 - len2 - 1 - i] + ex
            ex = 0
            if add[lena - len2 - 1 - i] > 9:
                ex = add[lena - len2 - 1 - i] // 10
                add[lena - len2 - 1 - i] -= 10
    if ex == 1:
        add[0] = 1
    while add[0] == 0 and len(add) > 1:
        add.remove(0)
    return add


def multip(str1, str2):
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    len1 = len(str1)
    len2 = len(str2)
    lenm = len1 + 1
    result = [0]
    for i in range(len2):
        multi = [0] * lenm
        ex = 0
        for j in range(len1):
            m = ex + str1[len1 - j - 1] * str2[len2 - i - 1]
            ex = 0
            if m > 9:
                ex = m // 10
                m = m % 10
            multi[lenm - j - 1] = m
        if ex != 0:
            multi[lenm - j - 1] = 1
        while multi[0] == 0 and len(multi) > 1:
            multi.remove(0)
        if i != 0:
            for j in range(i):
                multi.append(0)
        result = addition(result, multi)
    return result


def last(lst, n):
    if n < len(lst):
        # print(lst, lst[len(lst) - 1 - n])
        return lst[len(lst) - 1 - n]
    else:
        return 0


if __name__ == "__main__":
    # print(addition([1, 2, 5, 6, 9], [7, 8, 6]))
    # print(multip([1, 2, 5, 6, 9], [7, 8, 6]))
    str1 = [1, 0, 0]
    str2 = [1, 0]
    while str1 != [1, 0, 0, 0]:
        while str2 != [1, 0, 0]:
            res1 = multip(str1, [last(str2, 0)])
            str20 = [None] * 2
            str20[0] = last(str2, 1)
            str20[1] = 0
            res2 = multip(str1, str20)
            res3 = addition(res1, res2)
            if len(res3) > 4:
                continue
            col = [None] * 4
            for i in range(4):
                col[i] = last(str1, i) + last(str2, i) + last(res1, i) + last(res2, i) + last(res3, i)
            if col[0] == col[1] and col[0] == col[2] and col[0] == col[3]:
                print("".join(str1), " * ", "".join(str2), " = ", "".join(res3), ", all columns adding up to ", col[0])
            ###
            str2 = addition(str2, [1])
        str1 = addition(str1, [1])
