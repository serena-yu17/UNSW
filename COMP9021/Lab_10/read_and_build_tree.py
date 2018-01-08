import sys

with open("tree.txt")as f:
    lines = f.read().split('\n')

leng = 0

for line in lines:
    line = line.rstrip('\t')
    if len(line) > leng:
        leng = len(line)

tree_set = [None] * leng
for i in range(len(tree_set)):
    tree_set[i] = dict()

for l in range(len(lines)):
    depth = 0
    number = 0
    i = 0
    while i < len(lines[l]):
        num = 0
        while i < len(lines[l]) and lines[l][i].isdigit():
            if depth == 0:
                depth = i
            num *= 10
            num += int(lines[l][i])
            i += 1
        if num != 0:
            number = num
            break
        i += 1
    if number:
        while i < len(lines[l]):
            if lines[l][i].isdigit():
                print("tree.txt does not contain the correct representation of a tree.")
                sys.exit(1)
            i += 1
    if number:
        if tree_set[depth] is None:
            tree_set[depth] = list()
        tree_set[depth][l] = number



class Node:
    def __init__(self, val):
        self.val = val
        self.left = []
        self.right = []


depth = leng - 1
if len(tree_set[depth]) > 1:
    print("tree.txt does not contain the correct representation of a tree.")
    sys.exit(1)
line_num = next(iter(tree_set[depth]))
node_dic=dict()
node_dic[(depth, line_num)] = Node(tree_set[depth][line_num])
depth-=1
while depth > -1:
    for line_num in tree_set[depth]:
        if (depth+1, line_num-1) in node_dic:
            node_dic[(depth+1, line_num-1)].right.append(Node(tree_set[depth][line_num]))

    depth -= 1
