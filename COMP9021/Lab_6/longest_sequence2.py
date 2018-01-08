import sys

s = input("Please input a string of lowercase letters: ")
for ch in s:
    if ch < 'a' or ch > 'z':
        print("Invalid input")
        sys.exit()
s = tuple(map(ord, s))

maxlen = 0
maxstart = 0

def search(start):
    i = start
    count = 0
    ch = s[i]
    while i < len(s) and ch <= ord('z'):
        while i < len(s) and s[i] != ch + 1:
            i += 1
        count += 1
        ch += 1
    return count

letters = list()
letset = set()
for i in range(len(s)):
    if s[i] not in letset:
        letset.add(s[i])
        letters.append(i)
for start in letters:
    if start < len(s) - maxlen:
        count = search(start)
        if count > maxlen:
            maxlen = count
            maxstart = s[start]

print("The solution is: ", end='')
for i in range(maxstart, maxstart + maxlen):
    print(chr(i), end ='')
