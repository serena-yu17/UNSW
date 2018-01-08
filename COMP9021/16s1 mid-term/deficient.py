import sys


def is_def(num):
    i = num // 2 + 1
    sum = 0
    while i > 0:
        if num % i == 0:
            sum += i
            if sum >= num:
                return 0
        i -= 1
    return 1


if __name__ == "__main__":
    s = input("Enter two strictly positive numbers: ")
    s = s.split(" ")
    low = 0
    high = 0
    try:
        if len(s) != 2:
            raise ValueError
        if low <= 0 or high <= 0:
            raise ValueError
    except ValueError:
        print("Incorrect input, giving up.")
        sys.exit()
    incre = 1
    if high < low:
        incre = -1
    defi = []
    for i in range(low, high + incre, incre):
        if is_def(i):
            defi.append(i)
    if len(defi) == 0:
        print(f"There is no deficient number between {low} and {high}.")
    else:
        def1 = 0
        def2 = 0
        maxcount = 0
        for i in range(len(defi)):
            count = 1
            for j in range(i + 1, len(defi)):
                if defi[j] == defi[j - 1] + incre:
                    count += 1
                else:
                    if count > maxcount:
                        def1 = defi[i]
                        def2 = defi[j - 1]
                        maxcount = count
                    break

        print(f"The longest sequence of deficient numbers between {low} and {high} ranges between {def1} and {def2}.")
