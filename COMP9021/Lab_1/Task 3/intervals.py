from input_handler import input_handler
from random import seed, randrange

in_seed, nb_of_elements = input_handler()

seed(in_seed)
L = [randrange(0, 20) for _ in range(nb_of_elements)]
print("\nThe list is:", L, '\n')
count = [0] * 4
for elem in L:
    if elem < 5:
        count[0] += 1
    elif elem < 10:
        count[1] += 1
    elif elem < 15:
        count[2] += 1
    elif elem < 20:
        count[3] += 1
for i in range(0, 4):
    if count[i] == 0:
        count[i] = "is no element"
    elif count[i] > 1:
        count[i] = "are " + str(count[i]) + " elements"
    else:
        count[i] = "is 1 element"
    print("There ", count[i], "between", i * 5, "and", i * 5 + 4)
