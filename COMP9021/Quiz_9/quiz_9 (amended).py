# Generates a binary tree T whose shape is random and whose nodes store
# random even positive integers, both random processes being directed by user input.
# With M being the maximum sum of the nodes along one of T's branches, minimally expands T
# to a tree T* such that:
# - every inner node in T* has two children, and
# - the sum of the nodes along all of T*'s branches is equal to M.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange
from collections import defaultdict

from binary_tree_adt import *


def create_tree(tree, for_growth, bound):
    if randrange(max(for_growth, 1)):
        tree.value = 2 * randrange(bound + 1)
        tree.left_node = BinaryTree()
        tree.right_node = BinaryTree()
        create_tree(tree.left_node, for_growth - 1, bound)
        create_tree(tree.right_node, for_growth - 1, bound)


def dfs(tree):
    leaves = list()
    stack = list()
    used = defaultdict(int)
    stack.append(tree)
    max_sum = 0
    while len(stack):
        top = stack[-1]
        nxt = None
        child = 0
        if top not in used and top.left_node and top.left_node.value:
            nxt = top.left_node
            child = 1
        elif used[top] < 2 and top.right_node and top.right_node.value:
            nxt = top.right_node
            child = 2
        if nxt:
            stack.append(nxt)
            used[top] = child
        else:
            if not top.left_node or not top.left_node.value or not top.right_node or not top.right_node.value:
                sum_nodes = 0
                for node in stack:
                    sum_nodes += node.value
                leaves.append((top, sum_nodes))
                if sum_nodes > max_sum:
                    max_sum = sum_nodes
            stack.pop()
    return leaves, max_sum


def expand_tree(tree):
    if not tree or not tree.value or (
                (not tree.left_node or not tree.left_node.value) and (
                        not tree.right_node or not tree.right_node.value)):
        return
    leaves, max_sum = dfs(tree)
    for leaf in leaves:
        if leaf[1] < max_sum:
            if not leaf[0].left_node or not leaf[0].left_node.value:
                leaf[0].left_node = BinaryTree(max_sum - leaf[1])
            if not leaf[0].right_node or not leaf[0].right_node.value:
                leaf[0].right_node = BinaryTree(max_sum - leaf[1])


try:
    for_seed, for_growth, bound = [int(x) for x in input('Enter three positive integers: ').split()
                                   ]
    if for_seed < 0 or for_growth < 0 or bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
tree = BinaryTree()
create_tree(tree, for_growth, bound)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
expand_tree(tree)
print('Here is the expanded tree:')
tree.print_binary_tree()
