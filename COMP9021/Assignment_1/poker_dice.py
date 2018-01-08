from random import randint

#
#
dice_num = {"Ace": 0, "King": 1, "Queen": 2, "Jack": 3, "10": 4, "9": 5}
dice_name = ["Ace", "King", "Queen", "Jack", "10", "9"]
num = {"Five of a kind": 0, "Four of a kind": 1, "Full house": 2, "Straight": 3, "Three of a kind": 4, "Two pair": 5,
       "One pair": 6, "Bust": 7}
desc = ["Five of a kind", "Four of a kind", "Full house", "Straight", "Three of a kind", "Two pair", "One pair", "Bust"]
ordn = ["none", "first", "second", "third", "fourth", "fifth"]


#
#
def detect(rolls):
    rep = [0] * 6
    for fc in rolls:
        rep[fc] += 1
    max_rep = max(rep)
    if max_rep == 5:
        return 0
    if max_rep == 4:
        return 1
    if max_rep == 3:
        if 2 in rep:
            return 2
        else:
            return 4
    if max_rep == 2:
        count2 = 0
        for r in rep:
            if r == 2:
                count2 += 1
        if count2 == 2:
            return 5
        else:
            return 6
    if max_rep == 1:
        if set(rolls) == {1, 2, 3, 4, 5} or set(rolls) == {0, 1, 2, 3, 4}:
            return 3
        else:
            return 7


#
#
def play():
    counter = 1
    rolls = []
    for i in range(5):
        rolls.append(randint(0, 5))
    while 1:
        rolls.sort()
        print("The roll is: ", end="")
        for i in range(4):
            print(dice_name[rolls[i]], end=" ")
        print(dice_name[rolls[4]])
        word = detect(rolls)
        print("It is a", desc[word])
        counter += 1
        if counter == 4:
            return
        # keep dice
        #
        instruct = []
        in_dice = ""
        rep = 1
        while rep == 1:
            in_dice = input(f"Which dice do you want to keep for the {ordn[counter]} roll? ")
            if in_dice == "all" or in_dice == "All":
                print("Ok, done.")
                return
            if in_dice == "":
                break
            instruct = in_dice.split(" ")
            rep = 0
            for i in range(len(instruct)):
                if instruct[i] not in dice_name:
                    print("That is not possible, try again!")
                    instruct.clear()
                    rep = 1
                    break
                if dice_num[instruct[i]] not in rolls:
                    print("That is not possible, try again!")
                    instruct.clear()
                    rep = 1
                    break
            if len(instruct) > 5:
                print("That is not possible, try again!")
                instruct.clear()
                rep = 1
        if len(instruct) == 5:
            print("Ok, done.")
            return
        rolls.clear()
        if in_dice != "":
            for elem in instruct:
                rolls.append(dice_num[elem])
        for i in range(len(rolls), 5):
            rolls.append(randint(0, 5))


#
#
def simulate(n):
    if not isinstance(n, int):
        print("Invalid input, giving up...")
        return
    if n < 0:
        print("Invalid input, giving up...")
        return
    elif n > 0:
        stats = [0] * 8
        rolls = []
        for i in range(n):
            rolls.clear()
            for i in range(5):
                rolls.append(randint(0, 5))
            stats[detect(rolls)] += 1
    for i in range(7):
        if n > 0:
            possibility = stats[i] / sum(stats) * 100
        else:
            possibility = 0.0
        word = str(desc[i])
        if len(word) < 15:
            word += " " * (15 - len(word))
        print(f"{word}: {possibility:.2f}%")
