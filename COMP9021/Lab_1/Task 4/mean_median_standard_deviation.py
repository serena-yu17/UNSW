from input_handler import input_handler
from random import randrange, seed
from statistics import mean, median, pstdev


def mean_c(lst):
    if len(lst) == 0:
        return 0
    elif len(lst) == 1:
        return lst[0]
    else:
        return sum(lst) / len(lst)


def sort5(lst):
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            j = i
            while lst[j] > lst[i] and j > 0:
                j -= 1
            temp = lst[i]
            for k in range(j, i):
                lst[k + 1] = lst[k]
            lst[j] = temp
    return lst


def med_c(lst, offset):
    if len(lst) == 0:
        return 0
    if len(lst) == 1:
        return lst[0]
    if len(lst) < 6:
        lst = sort5(lst)
        return lst[offset]
    else:
        ls_index = [i for i in range(0, len(lst) + 5, 5)]
        med_5 = []
        for i in range(len(ls_index) - 1):
            med_5.append(med_c(lst[ls_index[i]:ls_index[i + 1]], int(len(lst[ls_index[i]:ls_index[i + 1]])/2)))
        pivot = med_c(med_5, int(len(med_5)/2))
        left = []
        right = []
        mid = []
        for elem in lst:
            if elem < pivot:
                left.append(elem)
            elif elem > pivot:
                right.append(elem)
            else:
                mid.append(elem)
        lst_med = range(len(left), len(left) + len(mid))
        if lst_med[0] > offset:
            return med_c(left, offset)
        elif lst_med[len(lst_med) - 1] < offset:
            return med_c(right, offset + len(left) + len(mid) - 1)
        else:
            return pivot


def med_sort(lst):
    lst = sorted(lst)
    len_ls = len(lst)
    if len_ls % 2 == 1:
        return lst[int(len_ls / 2)]
    else:
        return (lst[int(len_ls / 2)] + lst[int(len_ls / 2 - 1)]) / 2


def psd(lst):
    mean_ls = mean(lst)
    sd = 0
    for elem in lst:
        sd += (mean_ls - elem) ** 2
    return (sd / len(lst)) ** 0.5


in_seed, nb_of_elements = input_handler()
seed(in_seed)
ls_rand = [randrange(-50, 50) for _ in range(nb_of_elements)]
print("\nThe list is:\n", ls_rand)
if nb_of_elements % 2 == 1:
    med = med_c(ls_rand, int(nb_of_elements / 2))
else:
    med = (med_c(ls_rand, int(nb_of_elements / 2)) + med_c(ls_rand, int(nb_of_elements / 2) - 1)) / 2
print(f"The mean is: {mean_c(ls_rand):.2f}")
print(f"The median is: {med:.2f}")
print(f"The median through sorting is: {med_sort(ls_rand):.2f}")
print(f"The standard deviation is: {psd(ls_rand):.2f}")
print("\nConfirming from the statistics module:")
print(f"The median is: {mean(ls_rand):.2f}")
print(f"The median is: {median(ls_rand):.2f}")
print(f"The standard deviation is: {pstdev(ls_rand):.2f}")
