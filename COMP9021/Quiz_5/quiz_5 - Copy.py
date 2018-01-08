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
        path = [(x, y)]
        used = defaultdict(set)
        length = grid[y][x]
        while 1:
            if grid[y][x] == 1:
                nxt = None
            else:
                if x != 0 and grid[y][x - 1] == grid[y][x] - 1 and (x - 1, y) not in used[(x, y)]:
                    nxt = x - 1, y
                elif x != width - 1 and grid[y][x + 1] == grid[y][x] - 1 and (x + 1, y) not in used[(x, y)]:
                    nxt = x + 1, y
                elif y != 0 and grid[y - 1][x] == grid[y][x] - 1 and (x, y - 1) not in used[(x, y)]:
                    nxt = x, y - 1
                elif y != height - 1 and grid[y + 1][x] == grid[y][x] - 1 and (x, y + 1) not in used[(x, y)]:
                    nxt = x, y + 1
                else:
                    nxt = None
            if nxt == None:
                if grid[y][x] == 1:
                    count[length] += 1
                if len(path) == 1:
                    break
                path.pop()
                x, y = path[len(path) - 1]
            else:
                used[(x, y)].add(nxt)
                x, y = nxt
                path.append(nxt)
    return count


    #
    # end


for_seed = 0
lines = []
for i in range(20, 320, 20):
    max_length = i // 10
    height = width = i
    lines.append("\nEnter four nonnegative integers:{} {} {} {}\n".format(0, max_length, height, width))
    seed(for_seed)
    grid = [[randint(0, max_length) for _ in range(width)] for _ in range(height)]
    paths = get_paths()
    for i in range(len(paths)):
        if paths[i] != 0:
            lines.append('The number of paths from 1 to {} is: {}\n'.format(i, paths[i]))

with open("output.txt", 'w') as f:
    f.writelines(lines)
