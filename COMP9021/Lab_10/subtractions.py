def subtractions(tup, tar):
    if len(tup) == 0 or not isinstance(tup[0], int):
        return
    if len(tup) == 1:
        if tup[0] == tar:
            print(tar)
        return
    if len(tup) == 2:
        if tup[0] - tup[1] == tar:
            print("{} - {}".format(tup[0], tup[1]))
        return
    pos_nums = list()
    num = (1 << (len(tup) - 2)) - 1
    while num:
        line = [tup[0], -tup[1]]
        for i in range(2, len(tup)):
            if num & (1 << (i - 2)):
                line.append(tup[i])
            else:
                line.append(-tup[i])
        if sum(line) == tar:
            pos_nums.append(line)
        num -= 1
    for exp in pos_nums:
        combination = partition(0, exp)
        for exp in combination:
            print(exp)


def partition(depth, lst):
    if len(lst) < 3:
        for i in range(len(lst)):
            if i and lst[i] > 0:
                return None
        if len(lst) == 1:
            return [str(abs(lst[0]))]
        else:
            return ["({} - {})".format(abs(lst[0]), abs(lst[1]))]
    combinations = list()
    for i in range(len(lst)):
        if lst[i] < 0:
            part1 = lst[:i]
            part2 = list()
            for j in range(i, len(lst)):
                part2.append(-lst[j])
            part1 = partition(depth + 1, part1)
            part2 = partition(depth + 1, part2)
            if part1 and part2:
                for e1 in part1:
                    for e2 in part2:
                        if depth == 0:
                            exp = "{} - {}".format(e1, e2)
                        else:
                            exp = "({} - {})".format(e1, e2)
                        combinations.append(exp)
    return combinations


subtractions((1, 2, 3, 4, 5), 1)
print("---------")
subtractions((1, 2, 3, 4, 5), 3)
print("---------")
subtractions((1, 2, 3, 4, 5), 5)
print("---------")
subtractions((1, 3, 2, 5, 11, 9, 10, 8, 4, 7, 6), 40)
