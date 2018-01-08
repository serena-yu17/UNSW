def concate(grid):
    concat = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] is not None and grid[y][x] != 0:
                concat.append(grid[y][x])
    return concat


def gen_cycle(concat):
    cycles = []
    used = set()
    i = 0
    while i < len(concat):
        i = 0
        while i in used:
            i += 1
        cyc = []
        while i < len(concat) and i not in used:
            cyc.append(i + 1)
            used.add(i)
            i = concat[i] - 1
        if len(cyc) != 0:
            cycles.append(cyc)
    return cycles


def validate_9_puzzle(grid):
    if len(grid) != 3:
        print("This is an invalid or unsolvable 9 puzzle")
        return
    for ls in grid:
        if len(ls) != 3:
            print("This is an invalid or unsolvable 9 puzzle")
            return
    concat = concate(grid)
    if set(concat) != set(range(1, 9)):
        print("This is an invalid or unsolvable 9 puzzle")
        return	
    ncyc = gen_cycle(concat)
    print(ncyc)
    if len(ncyc) & 1 != 0:
        print("This is an invalid or unsolvable 9 puzzle")
        return
    print("This is a valid 9 puzzle, and it is solvable")


target = None

all_combin = set()


def horizontal(node, level):
    global all_combin
    lst = node.val
    i = 0
    while i < len(lst) and lst[i] != 0:
        i += 1
    if i % 3 == 0:
        lst = list(node.val)
        lst[i], lst[i + 1] = lst[i + 1], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    elif i % 3 == 1:
        lst = list(node.val)
        lst[i], lst[i + 1] = lst[i + 1], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
        lst = list(node.val)
        lst[i], lst[i - 1] = lst[i - 1], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    elif i % 3 == 2:
        lst = list(node.val)
        lst[i], lst[i - 1] = lst[i - 1], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    return None


def vertical(node, level):
    global all_combin
    lst = node.val
    i = 0
    while i < len(lst) and lst[i] != 0:
        i += 1
    if i // 3 == 0:
        lst = list(node.val)
        lst[i], lst[i + 3] = lst[i + 3], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    elif i // 3 == 1:
        lst = list(node.val)
        lst[i], lst[i + 3] = lst[i + 3], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
        lst = list(node.val)
        lst[i], lst[i - 3] = lst[i - 3], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    elif i // 3 == 2:
        lst = list(node.val)
        lst[i], lst[i - 3] = lst[i - 3], lst[i]
        lst = tuple(lst)
        if lst not in all_combin:
            all_combin.add(lst)
            new_node = Node(node)
            new_node.val = lst
            if lst == target:
                return new_node
            level.append(new_node)
    return None


class Node:
    def __init__(self, node):
        self.next = node
        self.val = None


def solve_9_puzzle(grid):
    initial = []
    for l in grid:
        for num in l:
            if num is None:
                num = 0
            initial.append(num)
    global target
    global all_combin
    target = tuple(initial)
    root = Node(None)
    root.val = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    found = None
    if target != root.val:
        all_combin.add(root.val)
        level = list()
        level.append(root)
        while found is None:
            newlevel = list()
            for node in level:
                found = horizontal(node, newlevel)
                if found is not None:
                    break
                found = vertical(node, newlevel)
                if found is not None:
                    break
            level = newlevel
    else:
        found = root
    if found is not None:
        print("Here is a minimal solution:\n")
    while found is not None:
        for i in range(3):
            print("  ", end='')
            for j in range(3):
                if j:
                    print(" ", end='')
                if found.val[i*3 + j]:
                    print(found.val[i*3 + j], end='')
                else:
                    print(" ", end='')
            print()
        found = found.next
        if found is not None:
            print()
        else:
            break
        

if __name__ == "__main__":
    while 1:
        s = input("Input your command: ")
        eval(s)
