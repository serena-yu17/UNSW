# Randomly generates N distinct integers with N provided by the user,
# inserts all these elements into a priority queue, and outputs a list
# L consisting of all those N integers, determined in such a way that:
# - inserting the members of L from those of smallest index of those of
#   largest index results in the same priority queue;
# - L is preferred in the sense that the last element inserted is as large as
#   possible, and then the penultimate element inserted is as large as possible, etc.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, sample
from math import log2

from priority_queue_adt import *

post_list = list()


def delete_elem(id):
    if testarr.is_empty():
        return
    if id > len(testarr):
        return
    if id != len(testarr):
        testarr._data[id], testarr._data[len(testarr)] = testarr._data[len(testarr)], testarr._data[id]
    testarr._length -= 1
    if id != len(testarr) + 1:
        testarr._bubble_down(id)


def valid(id):
    # store the original data setting
    data = testarr._data.copy()
    leng = len(testarr)
    del_elem = testarr._data[id]
    delete_elem(id)
    # keep a copy of the data after deletion
    del_data = testarr._data.copy()
    del_length = len(testarr)
    # try insert
    testarr.insert(del_elem)
    if len(testarr) == leng and testarr._data[:leng + 1] == data[:leng + 1]:
        # commit the deletion
        testarr._data = del_data
        testarr._length = del_length
        return del_elem
    # revert changes
    testarr._data = data
    testarr._length = leng
    return None


# Possibly define some functions

def preferred_sequence():
    seq = [0] * len(pq)
    pos = len(pq) - 1
    while pos != -1:
        i = 1
        while i < len(testarr) + 1:
            del_elem = valid(i)
            if del_elem is not None:
                seq[pos] = del_elem
                pos -= 1
                break
            i += 1
    return seq


# Replace pass above with your code (altogether, aim for around 24 lines of code)


try:
    for_seed, length = [int(x) for x in input('Enter 2 nonnegative integers, the second one '
                                              'no greater than 100: '
                                              ).split()
                        ]
    if for_seed < 0 or length > 100:
        raise ValueError
except ValueError:
    print('Incorrect input (not all integers), giving up.')
    sys.exit()
seed(for_seed)
L = sample(list(range(length * 10)), length)
pq = PriorityQueue()
for e in L:
    pq.insert(e)
testarr = PriorityQueue()
testarr._data = pq._data.copy()
testarr._length = len(pq)
print('The heap that has been generated is: ')
print(pq._data[: len(pq) + 1])
print('The preferred ordering of data to generate this heap by successsive insertion is:')
print(preferred_sequence())
