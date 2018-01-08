# Written by *** and Eric Martin for COMP9021

'''
Generates a list L of random nonnegative integers smaller than the length of L,
whose value is input by the user, and outputs two lists:
- a list M consisting of L's middle element, followed by L's first element,
  followed by L's last element, followed by L's second element, followed by
  L's penultimate element...;
- a list N consisting of L[0], possibly followed by L[L[0]], possibly followed by
  L[L[L[0]]]..., for as long as L[L[0]], L[L[L[0]]]... are unused, and then,
  for the least i such that L[i] is unused, followed by L[i], possibly followed by
  L[L[i]], possibly followed by L[L[L[i]]]..., for as long as L[L[i]], L[L[L[i]]]...
  are unused, and then, for the least j such that L[j] is unused, followed by L[j],
  possibly followed by L[L[j]], possibly followed by L[L[L[j]]]..., for as long as
  L[L[j]], L[L[L[j]]]... are unused... until all members of L have been used up.
'''

import sys
from random import seed, randrange

try:
    arg_for_seed, length = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length = int(arg_for_seed), int(length)
    if arg_for_seed < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randrange(length) for _ in range(length)]
print('\nThe generated list L is:')
print('  ', L)
M = []
N = []

# Replace this comment with your code
size = len(L)
if size == 0:
    pass
elif size == 1:
    M = L
    N = L
else:
    # fill M
    pivot = int(size / 2)
    M.append(L[pivot])
    i = 0
    j = size - 1
    while i != pivot or j != pivot:
        if i != pivot:
            M.append(L[i])
            i += 1
        if j != pivot:
            M.append(L[j])
            j -= 1
    # fill N
    used = [0] * size
    i = 0
    while i < size:
        used[i] = 1
        N.append(L[i])
        if used[L[i]] == 1:
            i = 0
            while i < size and used[i] == 1:
                i += 1
        else:
            i = L[i]
# End of my code
print('\nHere is M:')
print('  ', M)
print('\nHere is N:')
print('  ', N)
print('\nHere is L again:')
print('  ', L)
