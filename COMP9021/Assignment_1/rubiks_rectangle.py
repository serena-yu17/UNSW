#
import sys


#
def checkch(ch):
    return (ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' or ch == '8')


def checkL(lst):
    return lst == tuple(digits)


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


def seek(status):
    global steps
    global all
    new_sta = set()
    for stat in status:
        if checkL(stat):
            return 1, new_sta
        tup1 = row_exchange(stat)
        if checkL(tup1):
            steps += 1
            return 1, new_sta
        else:
            if tup1 not in all:
                new_sta.add(tup1)
        tup2 = right_shift(stat)
        if checkL(tup2):
            steps += 1
            return 1, new_sta
        else:
            if tup2 not in all:
                new_sta.add(tup2)
        tup3 = mid_clock(stat)
        if checkL(tup3):
            steps += 1
            return 1, new_sta
        else:
            if tup3 not in all:
                new_sta.add(tup3)
    steps += 1
    return 0, new_sta


def rev_low(lst):
    lst[4], lst[7] = lst[7], lst[4]
    lst[5], lst[6] = lst[6], lst[5]


# Input
#
str = input("Input final configuration: ")
digits = []
digset = set()
all = set()
for i in range(len(str)):
    if str[i] != " " and not checkch(str[i]):
        print("Incorrect configuration, giving up...")
        sys.exit()
    if checkch(str[i]):
        digits.append(int(str[i]))
        digset.add(int(str[i]))
if len(digset) != 8 and len(digits) == 8:
    print("Incorrect configuration, giving up...")
    sys.exit()
# processing
# from time import time
# start_time=time()
#
rev_low(digits)
steps = 0
status = {(1, 2, 3, 4, 8, 7, 6, 5)}
found = 0
while found == 0:
    found, status = seek(status)
    all = all | status
# Output
#
if steps == 0 or steps == 1:
    str_step = "step is"
else:
    str_step = "steps are"
print(steps, str_step, "needed to reach the final configuration.")
# print(f"Time taken: {time()-start_time}")
