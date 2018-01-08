import sys
from itertools import permutations
from collections import defaultdict

#
#
score = {'a': 2, 'b': 5, 'c': 4, 'd': 4, 'e': 1, 'f': 6, 'g': 5, 'h': 5, 'i': 1, 'j': 7, 'k': 6, 'l': 3, 'm': 5, 'n': 2,
         'o': 3, 'p': 5, 'q': 7, 'r': 2, 's': 1, 't': 2, 'u': 4, 'v': 6, 'w': 6, 'x': 7, 'y': 5, 'z': 7}


#
#
def score_str(st):
    scor = 0
    for ch in st:
        scor += score[ch]
    return scor


def getmaxp(s):
    s.sort(key=lambda ch: score[ch], reverse= True)
    maxp = []
    maxp.append(0)
    for i in range(1, len(s)+1):
        maxp.append(maxp[i - 1] + score[ss[i - 1]])
    return maxp


#
#
raw_str = input("Enter between 3 and 10 lowercase letters: ")
st = []
for i in range(len(raw_str)):
    if raw_str[i] != " ":
        if ord(raw_str[i]) < 97 or ord(raw_str[i]) > 122:
            print("Incorrect input, giving up...")
            sys.exit()
        else:
            st.append(raw_str[i])
if len(st) < 3 or len(st) > 10:
    print("Incorrect input, giving up...")
    sys.exit()
#
#
with open("wordsEn.txt") as file:
    words = set(file.read().split())
#
#
maxwords = set()
maxscore = 0
maxp = getmaxp(st)
i = len(st)
while maxp[i] > maxscore:
    for tup in permutations(st, i):
        word = "".join(tup)
        if word in words:
            scr = score_str(word)
            if scr > maxscore:
                maxwords.clear()
                maxscore = scr
                maxwords.add(word)
            elif scr == maxscore:
                maxwords.add(word)
    i -= 1
if len(maxwords) == 0:
    print("No word is built from some of those letters.")
else:
    maxwords = sorted(maxwords)
    print(f"The highest score is {maxscore}.")
    if len(maxwords) == 1:
        print(f"The highest scoring word is {maxwords[0]}")
    else:
        print("The highest scoring words are, in alphabetical order:")
        for w in maxwords:
            print(f"    {w}")
