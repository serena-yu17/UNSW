import sys

raw = input("Input a number that we will use as available digits: ")
raw.strip()
try:    
    digs = list(map(int, raw))
except ValueError:
    print("Invalid input, giving up...")
    sys.exit()
raw = input("Input a number that represents the desired sum: ")
try:
    target = int(raw)
except ValueError:
    print("Invalid input, giving up...")
    sys.exit()

solutions = set()        

def search(curSum, curDig):
    if curSum == target:
        solutions.add(tuple(curDig))
    elif curSum < target and len(curDig) < len(digs) - 1:
        for i in range(curDig[-1]+1, len(digs)):
            newSum = curSum + digs[i]
            newDig = curDig + [i]
            search(newSum, newDig)

for i in range(len(digs)):
    search(digs[i], [i])

if len(solutions) == 0:
    print("There is no solution.")
else:
    if len(solutions) == 1:
        print("There is a unique solution.")
    else:
        print("There are {} solutions.".format(len(solutions)))
    for comb in solutions:
        for i in range(len(comb)):
            if i:
                print(', ', end='')
            print(digs[comb[i]], end='')
        print()

    
