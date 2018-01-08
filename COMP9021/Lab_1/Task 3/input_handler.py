import sys


def input_handler():
    in_seed = input("Input your random seed:")
    try:
        in_seed = int(in_seed)
    except ValueError:
        input("Your input is not an integer. Press any key to exit")
        sys.exit()
    nb_of_elements = input("Input your number of elements:")
    try:
        nb_of_elements = int(nb_of_elements)
    except ValueError:
        input("Your input is not an integer. Press any key to exit")
        sys.exit()
    if nb_of_elements <= 0:
        input("The input has to be positive. Press any key to exit")
        sys.exit()
    return in_seed, nb_of_elements
