#


#
def checkch(ch):
    return (ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' or ch == '8')


def row_exchange(lst):
    new_lst = [None] * 8
    for i in range(4):
        new_lst[i], new_lst[i + 4] = lst[i + 4], lst[i]
    return tuple(new_lst)


def right_shift(lst):
    new_lst = [None] * 8
    for i in range(3):
        new_lst[i + 1] = lst[i]
        new_lst[i + 5] = lst[i + 4]
    new_lst[0] = lst[3]
    new_lst[4] = lst[7]
    return tuple(new_lst)


def mid_clock(lst):
    new_lst = [None] * 8
    new_lst[0] = lst[0]
    new_lst[4] = lst[4]
    new_lst[3] = lst[3]
    new_lst[7] = lst[7]
    new_lst[2] = lst[1]
    new_lst[6] = lst[2]
    new_lst[5] = lst[6]
    new_lst[1] = lst[5]
    return tuple(new_lst)


def next_lv(level):
    global steps
    new_sta = set()
    for stat in level:
        tup1 = row_exchange(stat)
        tup2 = right_shift(stat)
        tup3 = mid_clock(stat)
        new_sta.add(tup1)
        new_sta.add(tup2)
        new_sta.add(tup3)
    steps += 1
    return new_sta


if __name__ == "__main__":
    total = {}
    steps = 0
    level = {(1, 2, 3, 4, 8, 7, 6, 5)}
    total[(1, 2, 3, 4, 8, 7, 6, 5)] = steps
    while 1:
        level = next_lv(level)
        size = len(total)
        for elem in level:
            if not elem in total:
                total[elem] = steps
        if len(total) == size:
            print(steps)
            break
    out = [None] * 24
    for i in range(24):
        out[i] = list()
    for item in total:
        if item != None:
            out[total[item]].append(item)
    f = open("Rubiks.txt", 'w+')
    for i in range(24):
        f.write(str(out[i]) + '\n')
        print("Number of items after step",i, ':',len(out[i]))
    f.close()
