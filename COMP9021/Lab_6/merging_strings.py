import sys


def found():
    print(f"The {name} string can be obtained by merging the other two.")
    sys.exit(0)


def nosolution():
    print("No solution")
    sys.exit(0)


def next_letter(pos, pos1, pos2):
    if pos == len3 - 1:
        if pos1 < len1:
            for i in range(pos1, len1):
                if s1[i] == s3[pos]:
                    found()
        if pos2 < len2:
            for i in range(pos2, len2):
                if s2[i] == s3[pos]:
                    found()
        nosolution()
    else:
        if pos1 < len1:
            for i in range(pos1, len1):
                if s1[i] == s3[pos]:
                    next_letter(pos + 1, i + 1, pos2)
        if pos2 < len2:
            for i in range(pos2, len2):
                if s2[i] == s3[pos]:
                    next_letter(pos + 1, pos1, i + 1)


s1 = input("Please input the first string: ")
s2 = input("Please input the second string: ")
s3 = input("Please input the third string: ")
len1 = len(s1)
len2 = len(s2)
len3 = len(s3)
name = "third"
if len1 > len3:
    s1, s3 = s3, s1
    len1, len3 = len3, len1
    name = "first"
if len2 > len3:
    s2, s3 = s3, s2
    len2, len3 = len3, len2
    name = "second"

next_letter(0, 0, 0)
