# Randomly fills a grid of size height and width whose values are input by the user,
# with nonnegative integers randomly generated up to an upper bound N also input the user,
# and computes, for each n <= N, the number of paths consisting of all integers from 1 up to n
# that cannot be extended to n+1.
# Outputs the number of such paths, when at least one exists.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


class searchPoint:
    def __init__(self, a, b):
        self.x = a
        self.y = b
        self.used = set()


def get_paths():
    # start
    #
    # pre-process
    count = [0] * (max_length + 1)
    start = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                one = 1
                if y != 0 and grid[y - 1][x] == 2:
                    one = 0
                if x != 0 and grid[y][x - 1] == 2:
                    one = 0
                if x != width - 1 and grid[y][x + 1] == 2:
                    one = 0
                if y != height - 1 and grid[y + 1][x] == 2:
                    one = 0
                if one == 1:
                    count[1] += 1
            elif grid[y][x] > 1:
                large = 0
                if x != 0 and grid[y][x - 1] == grid[y][x] + 1:
                    large = 1
                elif y != height - 1 and grid[y + 1][x] == grid[y][x] + 1:
                    large = 1
                elif y != 0 and grid[y - 1][x] == grid[y][x] + 1:
                    large = 1
                elif x != width - 1 and grid[y][x + 1] == grid[y][x] + 1:
                    large = 1
                if large == 0:
                    start.add((x, y))
    # search
    for x, y in start:
        path = []
        length = grid[y][x]
        cur_point = searchPoint(x, y)
        path.append(cur_point)
        while 1:
            if grid[y][x] == 1:
                nxt = None
            else:
                if x != 0 and grid[y][x - 1] == grid[y][x] - 1 and (x - 1, y) not in path[len(path) - 1].used:
                    nxt = x - 1, y
                elif x != width - 1 and grid[y][x + 1] == grid[y][x] - 1 and (x + 1, y) not in path[len(path) - 1].used:
                    nxt = x + 1, y
                elif y != 0 and grid[y - 1][x] == grid[y][x] - 1 and (x, y - 1) not in path[len(path) - 1].used:
                    nxt = x, y - 1
                elif y != height - 1 and grid[y + 1][x] == grid[y][x] - 1 and (x, y + 1) not in path[
                            len(path) - 1].used:
                    nxt = x, y + 1
                else:
                    nxt = None
            if nxt == None:
                if grid[y][x] == 1:
                    count[length] += 1
                if len(path) == 1:
                    break
                path.pop()
                x, y = path[len(path) - 1].x, path[len(path) - 1].y
            else:
                new_point = searchPoint(nxt[0], nxt[1])
                path[len(path) - 1].used.add(nxt)
                x, y = nxt
                path.append(new_point)
    return count





    #
    # end


try:
    for_seed, max_length, height, width = [int(i) for i in
                                           input('Enter four nonnegative integers: ').split()
                                           ]
    if for_seed < 0 or max_length < 0 or height < 0 or width < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[randint(0, max_length) for _ in range(width)] for _ in range(height)]
print('Here is the grid that has been generated:')
display_grid()
paths = get_paths()
for i in range(len(paths)):
    if paths[i] != 0:
        print(f'The number of paths from 1 to {i} is: {paths[i]}')
