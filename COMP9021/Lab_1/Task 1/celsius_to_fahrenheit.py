# cel = 5/9 * (faren-32)


def to_faren(cel):
    return cel * 9 / 5 + 32


max_temp = 100
min_temp = 0
step = 20
print("Celcius\tFahrenheit")
for cel in range(min_temp, max_temp + step, step):
    print(f"{cel:7d}\t{to_faren(cel):10.1f}")
