op = [0] * 9  # 0 = NULL, 1 = '-', 2 = '+'


def incre(op):
    op[8] += 1
    if op[8] > 2:
        op[8] = 0
        ex = 1
        for i in range(1, 9):
            if ex == 0:
                break
            else:
                op[8 - i] += ex
                ex = 0
                if op[8 - i] > 2:
                    op[8 - i] = 0
                    ex = 1


def calc(num1, num2, op):
    if op == 1:
        return num1 - num2
    if op == 2:
        return num1 + num2


# format: x1x2x3x4x5x6x7x8x9
def calculate(lst):
    res = []
    if lst[0] == 0:
        lst[0] = 2
    i = 0
    while i < 9:
        pos = 1
        if lst[2 * i] == 1:
            pos = -1
        buffer = int(lst[2 * i + 1])
        i += 1
        while i < 9 and lst[2 * i] == 0:
            buffer *= 10
            buffer += int(lst[2 * i + 1])
            i += 1
        res.append(buffer * pos)
    if lst[0] == 2:
        lst[0] = 0
    sum = 0
    for elem in res:
        sum += elem
    return sum


num = list(range(1, 10))
while op[0] < 2:
    exp = []
    for i in range(9):
        exp.append(op[i])
        exp.append(num[i])
    incre(op)
    sum = calculate(exp)
    if sum == 100:
        s = []
        if exp[0] != 1:
            s.append(" ")
        else:
            s.append("-")
        s.append(str(exp[1]))
        for i in range(1, 9):
            if exp[2 * i] == 1:
                s.append(' - ')
            if exp[2 * i] == 2:
                s.append(' + ')
            s += str(exp[2 * i + 1])
        print("".join(s), "= 100")
