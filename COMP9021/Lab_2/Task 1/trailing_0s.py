from math import factorial, log, pow


def gcd(a, b):
    if a == b:
        return a
    if a < b:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


def smt(int_in):
    # create the next power of 5 larger than the input integer
    pow5 = int(5 ** (log(int_in) // log(5) + 1))
    end5 = 0
    for i in range(1, int_in + 1):
        g = gcd(i, pow5)
        if g > 1:
            end5 += int(log(g) / log(5))  # how many factors of 5 are included
    return end5


def div(int_in):
    fac = factorial(int_in)
    zero_count = 0
    while fac % 10 == 0:
        zero_count += 1
        fac = fac // 10
    return zero_count


def ist(int_in):
    int_fac = factorial(int_in)
    str_fac = str(int_fac)
    i = len(str_fac) - 1
    zero_count = 0
    while str_fac[i] == '0':
        zero_count += 1
        i -= 1
    return zero_count


while 1:
    int_input = input("Input a nonnegative integer:")
    try:
        int_input = int(int_input)
    except ValueError:
        print("Incorrect input, giving up.")
        continue
    if (int_input < 0):
        print("Incorrect input, giving up.")
        continue
    int_div = div(int_input)
    int_str = ist(int_input)
    int_smt = smt(int_input)
    print(f"Computing the number of trailing 0s in {int_input}! by dividing by 10 for long enough: {int_div}")
    print(f"Computing the number of trailing 0s in {int_input}! by converting it into a string: {int_str}")
    print(f"Computing the number of trailing 0s in {int_input}! the smart way: {int_smt}")
