# Written by *** and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers, the largest possible value
and the length of L being input by the user, and generates:
- a list "fractions" of strings of the form 'a/b' such that:
    . a <= b;
    . a*n and b*n both occur in L for some n
    . a/b is in reduced form
  enumerated from smallest fraction to largest fraction
  (0 and 1 are exceptions, being represented as such rather than as 0/1 and 1/1);
- if "fractions" contains then 1/2, then the fact that 1/2 belongs to "fractions";
- otherwise, the member "closest_1" of "fractions" that is closest to 1/2,
  if that member is unique;
- otherwise, the two members "closest_1" and "closest_2" of "fractions" that are closest to 1/2,
  in their natural order.
'''

import sys
from math import gcd
from random import seed, randint

try:
    arg_for_seed, length, max_value = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 0 or length < 0 or max_value < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, max_value) for _ in range(length)]
if not any(e for e in L):
    print('\nI failed to generate one strictly positive number, giving up.')
    sys.exit()

print('\nThe generated list is:')
print('  ', L)

fractions = []
spot_on, closest_1, closest_2 = [None] * 3
'''
from time import time
start=time()'''
# Replace this comment with your code
##
##

frac = set()
L.sort()
i = 0
zero = 0
while L[zero] == 0:
    zero += 1
while i < len(L) - 1:
    j = max(i + 1, zero)
    while j < len(L):
        if L[j] != 0:
            if L[i] != 0:
                num1 = L[i] // gcd(L[i], L[j])
                num2 = L[j] // gcd(L[i], L[j])
                value = num1 / num2
            else:
                num1 = 0
                num2 = 0
                value = 0.0
            frac.add((num1, num2, value))
        j += 1
    i += 1
if (1, 1, 1.0) not in frac:
    frac.add((1, 1, 1))
if (1, 2, 0.5) in frac:
    spot_on = 1
frac = list(frac)
frac.sort(key=lambda tup: tup[2])
for tup in frac:
    if tup[2] != 1 and tup[2] != 0:
        fractions.append(f"{tup[0]}/{tup[1]}")
    else:
        fractions.append(f"{tup[0]}")
if spot_on != 1:
    first = 0
    last = len(frac) - 1
    while last > first + 1:
        if frac[int((first + last) / 2)][2] < 0.5:
            first = int((first + last) / 2)
        else:
            last = int((first + last) / 2)
    if abs(frac[first][2] - 0.5) > abs(frac[last][2] - 0.5):
        first = last
    if frac[first][2] == 0:
        closest_1 = '0'
    elif frac[first][2] == 1:
        closest_1 = '1'
    else:
        closest_1 = f"{frac[first][0]}/{frac[first][1]}"
    if first + 1 < len(frac) and frac[first + 1][1] == frac[first][1] and frac[first + 1][0] + frac[first][0] == \
            frac[first + 1][1]:
        if frac[first + 1][2] == 0:
            closest_2 = '0'
        elif frac[first + 1][2] == 1:
            closest_2 = '1'
        else:
            closest_2 = f"{frac[first+1][0]}/{frac[first+1][1]}"
    elif first - 1 >= 0 and frac[first - 1][1] == frac[first][1] and frac[first - 1][0] + frac[first][0] == \
            frac[first - 1][1] < 0.0001:
        if frac[first - 1][2] == 0:
            closest_2 = '0'
        elif frac[first - 1][2] == 1:
            closest_2 = '1'
        else:
            closest_2 = f"{frac[first-1][0]}/{frac[first-1][1]}"

# end of my code
# end=time()

print('\nThe fractions no greater than 1 that can be built from L, from smallest to largest, are:')
print('  ', '  '.join(e for e in fractions))
if spot_on:
    print('One of these fractions is 1/2')
elif closest_2 is None:
    print('The fraction closest to 1/2 is', closest_1)
else:
    print(closest_1, 'and', closest_2, 'are both closest to 1/2')

# print("Elapsed time:", end-start)
