while 1:
    int_input = input("Input a nonnegative integer:")
    try:
        int_input = int(int_input)
    except ValueError:
        print("Incorrect input, giving up.")
        continue
    if int_input <= 0:
        print("Incorrect input, giving up.")
        continue
    perf = []
    for i in range(2, int_input):
        sum = 0
        for j in range(1, i // 2 + 1):
            if i % j == 0:
                sum += j
        if sum == i:
            perf.append(i)
    for elem in perf:
        print(elem, " is a perfect number.")
