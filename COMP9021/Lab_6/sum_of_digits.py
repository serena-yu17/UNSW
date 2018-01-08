import sys


def next_digit(cur_sum, pos):
    global count
    if cur_sum + nums[pos] == sum:
        count += 1
        return
    elif cur_sum + nums[pos] > sum:
        return
    else:
        if pos == leng - 1:
            return
        else:
            cur_sum += nums[pos]
            for i in range(pos + 1, leng):
                next_digit(cur_sum, i)


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
for i in range(leng):
    if nums[i] == sum:
        count += 1
    else:
        if i != leng - 1:
            cur_sum = nums[i]
            for j in range(i + 1, leng):
                next_digit(cur_sum, j)
if count == 0:
    print("There is no solution.")
elif count == 1:
    print("There is a unique solution.")
elif count > 1:
    print("There are {} solutions".format(count))
