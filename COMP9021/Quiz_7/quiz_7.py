# Generates a linked list of a length determined by user input,
# consisting of random nonnegative integers whose upper bound is also determined
# by user input, and reorders the list so that it starts with all odd values and
# ends with all even values, preserving the order of odd and even values in the
# original list, respectively.
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, randrange
from extended_linked_list import ExtendedLinkedList


def collect_references(L, length):
    node = L.head
    references = set()
    for i in range(length):
        references.add(id(node))
        node = node.next_node
    return references

try:
    for_seed, length, upper_bound = [int(i) for i in input('Enter three nonnegative integers: '
                                                          ).split()
                                    ]                                     
    if for_seed < 0 or length < 0 or upper_bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
LL = ExtendedLinkedList([randrange(upper_bound + 1) for _ in range(length)])
LL.print()
references = collect_references(LL, length)
LL.rearrange()
if collect_references(LL, length) != references:
    print('You cheated!')
    sys.exit()
else:
    LL.print()
