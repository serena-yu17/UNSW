from math import sqrt

# global variables
#
dice = [3, 2, 1]
SUM = 7  # sum of opposite faces


# functions
#
def roll_right(n):
    stp = n & 3
    if stp == 0:
        return
    if stp == 1:
        temp = dice[0]
        dice[0] = SUM - dice[2]
        dice[2] = temp
        return
    if stp == 2:
        dice[0] = SUM - dice[0]
        dice[2] = SUM - dice[2]
        return
    if stp == 3:
        temp = dice[0]
        dice[0] = dice[2]
        dice[2] = SUM - temp
        return


def roll_left(n):
    stp = n & 3
    if stp == 0:
        return
    return roll_right(4 - stp)


def roll_up(n):
    stp = n & 3
    if stp == 0:
        return
    if stp == 1:
        temp = dice[0]
        dice[0] = dice[1]
        dice[1] = SUM - temp
        return
    if stp == 2:
        dice[0] = SUM - dice[0]
        dice[1] = SUM - dice[1]
        return
    if stp == 3:
        temp = dice[1]
        dice[1] = dice[0]
        dice[0] = SUM - temp
        return


def roll_down(n):
    stp = n & 3
    if stp == 0:
        return
    return roll_up(4 - stp)


def roll(n):
    if direction == 0:
        roll_right(n)
    elif direction == 1:
        roll_down(n)
    elif direction == 2:
        roll_left(n)
    elif direction == 3:
        roll_up(n)


def dice_str():
    return f"{dice[0]} is at the top, {dice[1]} at the front, and {dice[2]} on the right."


def turn():
    global direction
    global turns
    turns += 1
    direction += 1
    if direction > 3:
        direction = 0


# main
#
# Input
#
ub = ""
while ub == "":
    ub = input("Enter the desired goal cell number: ")
    try:
        ub = int(ub)
    except ValueError:
        print("Incorrect value, try again")
        ub = ""
        continue
    if ub <= 0:
        print("Incorrect value, try again")
        ub = ""

# Rolling
#
incre = int(((sqrt(ub) - 1) // 6) * 6 + 1)
pos = incre ** 2
turns = 0
direction = 0  # 0 = right, 1 = down, 2 = left, 3 = up
if ub > pos + 1:
    pos += 1
    roll(1)
    turn()
    while pos < ub - incre:
        pos += incre
        roll(incre)
        turn()
        if turns & 1 == 0:
            incre += 1
roll(ub - pos)
# Print
#
d_str = dice_str()
print(f"On cell {ub},", d_str)
