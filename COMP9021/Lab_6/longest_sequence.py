def search(pos, asc, length):
    global maxlength, maxend
    if ord(string[pos]) == asc:
        if pos != leng - 1:
            for i in range(pos, leng):
                if ord(string[i]) == asc + 1:
                    search(i, asc + 1, length + 1)
    if length > maxlength:
        maxlength = length
        maxend = asc


string = input("Please input a string of lowercase letters: ")
leng = len(string)
maxlength = 0
maxend = 0
for i in range(leng):
    search(i, ord(string[i]), 0)
solution = [chr(i) for i in range(maxend - maxlength, maxend + 1)]
solution = "".join(solution)
print("The solution is: {}".format(solution))
