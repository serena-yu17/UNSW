ub = None
while ub == None:
    ub = input("Enter strictly positive number: ")
    try:
        ub = int(ub)
    except ValueError:
        print("Invalid value, re-enter.")
    if ub < 1:
        ub = None
        print("Invalid value, re-enter.")
letters = [None] * ub
let = ord('A')
for i in range(ub):
    letters[i] = [None] * (i + 1)
    for j in range(i + 1):
        letters[i][j] = chr(let)
        let += 1
        if let > ord('Z'):
            let = ord('A')
for i in range(ub):
    print(' ' * (ub-i), end="")
    for j in range(i + 1):
        print(letters[i][j], end="")
    if i > 0:
        for j in range(i - 1, -1, -1):
            print(letters[i][j], end="")
    print()
