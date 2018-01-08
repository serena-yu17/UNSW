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
from random import seed, randrange


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.used = [0] * 4
        self.direction = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return (self.x << 16) | self.y


def explore_depth_first(x, y, target):
    if sum_grid() < target:
        return None
    sm = grid[x][y]
    if sm == target:
        return [(x, y)]
    direction = 0
    root = point(x, y)
    stack_set = {root}
    stack = [root]
    while len(stack) != 0:
        nxt = None
        pt = stack[-1]
        if sm < target:
            for i in range(4):
                if direction == 3:
                    if pt.y == 0 or pt.used[direction] == 1:
                        nxt = None
                    else:
                        nxt = point(pt.x, pt.y - 1)
                        nxt.used[1] = 1
                        if nxt in stack_set:
                            nxt = None
                elif direction == 2:
                    if pt.x == len(grid) - 1 or pt.used[direction] == 1:
                        nxt = None
                    else:
                        nxt = point(pt.x + 1, pt.y)
                        nxt.used[0] = 1
                        if nxt in stack_set:
                            nxt = None
                elif direction == 1:
                    if pt.y == len(grid) - 1 or pt.used[direction] == 1:
                        nxt = None
                    else:
                        nxt = point(pt.x, pt.y + 1)
                        nxt.used[3] = 1
                        if nxt in stack_set:
                            nxt = None
                elif direction == 0:
                    if pt.x == 0 or pt.used[direction] == 1:
                        nxt = None
                    else:
                        nxt = point(pt.x - 1, pt.y)
                        nxt.used[2] = 1
                        if nxt in stack_set:
                            nxt = None
                if nxt:
                    break
                direction += 1
                if direction == 4:
                    direction = 0
        if nxt:
            stack[-1].direction = direction
            stack[-1].used[direction] = 1
            stack.append(nxt)
            stack_set.add(nxt)
            sm += grid[nxt.x][nxt.y]
            if sm == target:
                return gen_list(stack)
        else:
            sm -= grid[stack[-1].x][stack[-1].y]
            stack_set.remove(stack[-1])
            stack.pop()
            if len(stack):
                direction = stack[-1].direction
    return None


def sum_grid():
    sm = 0
    for y in range(10):
        sm += sum(grid[y])
    return sm


def gen_list(lst):
    out = []
    for pt in lst:
        out.append((pt.x, pt.y))
    return out


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
path = explore_depth_first(x, y, target)
if not path:
    print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
else:
    print('With North as initial direction, and exploring the space clockwise,')
    print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
    print(path)
