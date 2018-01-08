from collections import defaultdict

words = set()
with open("text_file.txt") as f:
    txt = f.read()
    i = 0
    while i < len(txt):
        buffer = []
        while i < len(txt) and \
                ((txt[i].lower() <= 'z' and txt[i].lower() >= 'a') or txt[i] == '-'):
            buffer.append(txt[i].lower())
            i += 1
        if len(buffer) > 0:
            words.add(tuple(buffer))
        buffer.clear()
        i += 1
s = input("Enter characters (spaces will be ignored): ")
letters = set()
i = 0
while i < len(s):
    if (s[i].lower() <= 'z' and s[i].lower() >= 'a') or s[i] == '-':
        letters.add(s[i].lower())
    i += 1
lenwords = defaultdict(set)
for w in words:
    if set(w).issubset(letters):
        lenwords[len(w)].add("".join(w))
for leng in sorted(lenwords):
    print("Words of length {} built from these characters, in lexicographic order:".format(leng))
    for w in sorted(lenwords[leng]):
        print("   ", w)
