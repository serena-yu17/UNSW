# Randomly fills a grid of size 10 x 10 with digits between 0
# and bound - 1, with bound provided by the user.
# Given a point P of coordinates (x, y) and an integer "target"
# also all provided by the user, finds a path starting from P,
# moving either horizontally or vertically, in either direction,
# so that the numbers in the visited cells add up to "target".
# The grid is explored in a depth-first manner, first trying to move north,
# always trying to keep the current direction,
# and if that does not work turning in a clockwise manner.
#
# Written by Eric Martin for COMP9021


import sys
import os.path
from random import seed, randrange
from ctypes import WinDLL, create_string_buffer, c_int, byref, POINTER, c_char_p
from time import time


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

try:
    for_seed, bound, x, y, target = [int(x) for x in input('Enter five integers: ').split()]
    if bound < 1 or x not in range(10) or y not in range(10) or target < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(bound) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()


dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pydll.dll")
dfsdll = WinDLL(dll_path)
dfsdll.DFS.restype = None
grid_arr = (c_int * 10) * 10
dfsdll.DFS.argtypes = [c_char_p, POINTER(grid_arr), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
c_grid = grid_arr()
for j in range(10):
    for i in range(10):
        c_grid[j][i] = grid[j][i]
c_x = c_int(x)
c_y = c_int(y)
c_target = c_int(target)
paths = create_string_buffer(1000)

time1 = time()
dfsdll.DFS(paths, byref(c_grid), byref(c_x), byref(c_y), byref(c_target))
time2 = time()
paths = paths.value.decode("ascii")

if not len(paths):
    print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
else:
    print('With North as initial direction, and exploring the space clockwise,')
    print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
    print(paths)
print("Time elapsed: ", time2 - time1)
