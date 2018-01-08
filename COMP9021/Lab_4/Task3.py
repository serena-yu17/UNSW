direction = 0  # 0 = up, 1 = left, 2 = down, 3 = right


def move(pos, n):
    if n == 0:
        return
    if direction == 0:
        pos[1] = pos[1] + n
        return
    if direction == 1:
        pos[0] = pos[0] - n
        return
    if direction == 2:
        pos[1] = pos[1] - n
        return
    if direction == 3:
        pos[0] = pos[0] + n
        return


def turn():
    global direction
    direction += 1
    if direction > 3:
        direction = 0


def decode(number):
    if number == 0:
        return (0, 0)
    sq = int(number ** 0.5)
    incre = (sq - (sq & 1 ^ 1)) + 1
    num = (incre - 1) ** 2
    pos = [int(incre / 2), 1 - int(incre / 2)]
    global direction
    direction = 0
    if number < num + incre - 1:
        move(pos, number - num)
        return tuple(pos)
    else:
        num += incre - 1
        move(pos, incre - 1)
        turn()
    while number > num + incre:
        num += incre
        move(pos, incre)
        turn()
    move(pos, number - num)
    return tuple(pos)


def encode(x, y):
    if x == 0 and y == 0:
        return 0
    ring = max(abs(x), abs(y))
    incre = 2 * ring
    num = ((ring - 1) * 2 + 1) ** 2
    pivot = [int(incre / 2), 1 - int(incre / 2)]
    if x == pivot[0]:
        if y >= pivot[1]:
            return num + y - pivot[1]
        else:
            return num + incre * 4 - 1
    num += incre - 1
    pivot[1] += incre - 1
    if y == pivot[1]:
        num += pivot[0] - x
        return num
    pivot[0] -= incre
    num += incre
    if x == pivot[0]:
        num += pivot[1] - y
        return num
    pivot[1] -= incre
    num += incre
    if y == pivot[1]:
        num += x - pivot[0]
        return num


if __name__ == "__main__":
    inp = input("Enter a number an encode: ")
    i = 0
    num = []
    while i < len(inp):
        while i < len(inp) and not (inp[i].isdigit() or inp[i] == '-'):
            i += 1
        j = i
        while j < len(inp) and (inp[j].isdigit() or inp[j] == '-'):
            j += 1
        num.append(int(inp[i:j]))
        i += j
    print(encode(num[0], num[1]))
