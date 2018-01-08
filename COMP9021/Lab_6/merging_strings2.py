s1 = input("Please input the first string: ")
s2 = input("Please input the second string: ")
s3 = input("Please input the third string: ")

n = "third"
if len(s3) < len(s1):
    s3, s1 = s1, s3
    n = "first"
if len(s3) < len(s2):
    s3, s2 = s2, s3
    n = "second"

s1 = list(s1)
s2 = list(s2)
s3 = list(s3)

def search(lst, id1, id2):
    if lst == s3:
        return 1
    if len(lst) < len(s3):
        if id1 + 1 < len(s1):
            for i in range(id1+1, len(s1)):
                if s1[i] == s3[len(lst)]:
                    newlst = lst + [s1[i]]
                    if search(newlst, i, id2):
                        return 1
        if id2 + 1 < len(s2):
            for i in range(id2+1, len(s2)):
                if s2[i] == s3[len(lst)]:
                    newlst = lst + [s2[i]]
                    if search(newlst, id1, i):
                        return 1
        return 0

found = search(list(),-1, -1)
if (found):
    print("The {} string can be obtained by merging the other two.".format(n))
else:
    print("No solution")

    

