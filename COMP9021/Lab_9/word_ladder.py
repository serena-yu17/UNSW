index = dict()
words = list()

counter = 0
with open("dictionary.txt") as f:
    for wd in f.read().split('\n'):
        index[wd] = counter
        counter += 1
        words.append(wd)


def build_candidates(id):
    wd = words[id]
    cand = [None] * len(wd)
    for i in range(len(wd)):
        cand[i] = list()
        for j in range(ord('A'), ord('Z') + 1):
            if j != ord(wd[i]):
                nxt = list()
                for k in range(i):
                    nxt.append(wd[k])
                nxt.append(chr(j))
                if i != len(wd) - 1:
                    for k in range(i + 1, len(wd)):
                        nxt.append(wd[k])
                nxt = ''.join(nxt)
                if nxt in index:
                    cand[i].append(index[nxt])
    return cand

class Node:
    def __init__(self, wd, last, position):
        self.id = wd
        self.last = last
        self.position = position


def word_ladder(s1, s2):
    s1 = s1.upper()
    s2 = s2.upper()
    if not len(s1) or not len(s2) or s1 not in index or s2 not in index or len(s1) != len(s2):
        return list()
    cand_dict = dict()
    chains = list()
    root = Node(index[s1], None, -1)
    level = [root]
    while not len(chains):
        level = bfs(level, index[s2], chains, cand_dict)
    return id_to_wd(chains)



def bfs(level, target, chains, cand_dict):
    new_level = list()
    for nd in level:
        wd = nd.id
        if wd not in cand_dict:
            cand_dict[wd] = build_candidates(wd)
        for i in range(len(words[target])):
            if i != nd.position:
                for cand in cand_dict[wd][i]:
                    new_node = Node(cand, nd, i)
                    if cand == target:
                        chains.append(new_node)
                    new_level.append(new_node)
    return new_level


def id_to_wd(ld):
    ladders = list()
    for nd in ld:
        w_lst = list()
        front = nd
        while front:
            w_lst.append(words[front.id])
            front=front.last
        w_lst.reverse()
        ladders.append(w_lst)
    return ladders


if __name__ == "__main__":
    s = input("Input words: ").split(' ')
    for lst in word_ladder(s[0], s[1]):
        print(lst)
