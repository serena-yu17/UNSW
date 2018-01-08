##
import random

##
##


dice = {0: 4, 1: 6, 2: 8, 3: 12, 4: 20}
tosses = []
exceed = [0] * 5


def toss(n_dice):
    rnd = random.SystemRandom()
    rnd_int = rnd.randint(1, dice[n_dice])
    tosses.append(rnd_int)
    return rnd_int


# n_dice: sides of the current dice being calculated. n_toss: nth toss of the current toss, e.g. 2nd, 4th
def bayes(n_dice, n_toss):
    n_toss += 1
    if exceed[n_dice] == 1:
        return 0.0
    n = 0
    for elem in exceed:
        if elem == 1:
            n += 1
    div = 0
    for i in range(n, 5):
        div += 1 / (dice[i] ** n_toss)
    bys = 1 / (dice[n_dice] ** n_toss) / div
    return bys * 100


while 1:
    tosses.clear()
    exceed = [0] * 5
    n_time = input("\nEnter the desired number of times a randomly chosen die will be cast:")
    try:
        n_time = int(n_time)
    except ValueError:
        print("Invalid number, giving up.")
    if n_time <= 0:
        print("Invalid number, giving up.")
    rnd = random.SystemRandom()
    sec_dice = rnd.randint(0, 4)
    print("This is a secret, but the chosen die is the one with ", dice[sec_dice], " faces")
    bay = [0.0] * 5
    for i in range(n_time):
        cur_toss = toss(sec_dice)
        for j in range(5):
            if dice[j] < cur_toss:
                exceed[j] = 1
                bay[j] = 0
            else:
                bay[j] = bayes(j, i)
        if i < 5:
            print("Casting the chosen die... Outcome: ", cur_toss)
            print("The updated dice probabilities are:")
            for j in range(0, 5):
                print(f"{dice[j]}: {bay[j]:0.2f}%")
    if n_time > 5:
        print("The final probabilities are:")
        for j in range(0, 5):
            print(f"{dice[j]}: {bay[j]:0.2f}%")
