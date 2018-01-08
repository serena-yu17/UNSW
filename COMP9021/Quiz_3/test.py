# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for given step_number >= 1
# and step_size >= 2, the number of stairs of step_number many steps,
# with all steps of size step_size.
#
# A stair of 1 step of size 2 is of the form
# 1 1
#   1 1
#
# A stair of 2 steps of size 2 is of the form
# 1 1
#   1 1
#     1 1
#
# A stair of 1 step of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#
# A stair of 2 steps of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#         1
#         1 1 1
#
# The output lists the number of stairs from smallest step sizes to largest step sizes,
# and for a given step size, from stairs with the smallest number of steps to stairs
# with the largest number of stairs.
#
# Written by *** and Eric Martin for COMP9021


import sys
from collections import defaultdict
from random import seed, randint
from time import time



# Replace return {} above with your code
head = set()
time1 = 0
time2 = 0


# Possibly define other functions
def search(x, y, sz):
    local_used = None
    for i in range(sz - 1):
        if x == dim - 1 or grid[y][x] == 0:
            return 0, local_used
        else:
            x += 1
    count = 0
    while x < dim-sz+1 and y < dim-sz+1:
        yub = y + sz - 1
        while y < yub:
            if grid[y][x] == 0:
                return count, local_used
            else:
                y += 1
        if y < dim and grid[y][x] != 0:
            if local_used is None:
                local_used = {(x, y)}
            else:
                local_used.add((x, y))
        else:
            return count, local_used
        xub = x + sz - 1
        while x < xub:
            if grid[y][x] == 0:
                return count, local_used
            else:
                x += 1
            if grid[y][x] == 0:
                return count, local_used
        count += 1
    return count, local_used


def find_stairs():
    global time1
    time1 = time()
    maxsize = 3 + dim // 2
    global used
    for sz in range(2, dim // 2 + 1):
        points = set()
        for y in range(dim - sz + 1):
            for x in range(dim - sz):
                if grid[y][x] != 0 and grid[y][x + 1] != 0 and (x, y) not in points:
                    count, local_used = search(x, y, sz)
                    if count > 0:
                        head.add((x, y))
                        points = points | local_used
                        if used[sz] is None:
                            used[sz] = [0] * (dim - sz)
                        used[sz][count] += 1
    global time2
    time2 = time()


# end

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]


def display_grid():
    for y in range(len(grid)):
        for x in range(len(grid)):
            if (x, y) in head:
                print('\033[91m' + str(int(grid[y][x] != 0)) + '\033[0m', end=' ')
            else:
                print(int(grid[y][x] != 0), end=' ')
        print()


used = [None] * (3 + dim // 2)
find_stairs()

print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are step sizes, and whose values are pairs of the form
# (number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size),
# ordered from smallest to largest number_of_steps.




for sz in range(2, len(used)):
    if used[sz] is not None:
        print(f'\nFor steps of size {sz}, we have:')
        for count in range(len(used[sz])):
            if used[sz][count] != 0:
                stair_or_stairs = 'stair' if  used[sz][count] == 1 else 'stairs'
                step_or_steps = 'step' if count == 1 else 'steps'
                print(f'     {used[sz][count]} {stair_or_stairs} with {count} {step_or_steps}')

print("Time: ",time2 - time1)
