import sys


def incre():
    global pattern
    add = 1
    i = 0
    while i < leng and add == 1:
        pattern[i] += add
        add = 0
        if pattern[i] == 2:
            pattern[i] = 0
            add = 1
        i += 1


def notend():
    notend = 0
    for i in range(leng):
        if pattern[i] != 0:
            notend = 1
    return notend


s1 = input("Input a number that we will use as available digits: ")
nums = list()
s2 = input("Input a number that represents the desired sum: ")
sum = 0
try:
    for i in range(len(s1)):
        nums.append(int(s1[i]))
    sum = int(s2)
except ValueError:
    print("Invalid input, giving up...")
    sys.exit(0)
count = 0
leng = len(nums)
pattern = [0] * leng
pattern[0] = 1
while notend():
    t_sum = 0
    for i in range(leng):
        if pattern[i] == 1:
            t_sum += nums[i]
    if t_sum == sum:
        count += 1
    incre()

if count == 0:
    print("There is no solution.")
elif count == 1:
    print("There is a unique solution.")
elif count > 1:
    print("There are {} solutions".format(count))
