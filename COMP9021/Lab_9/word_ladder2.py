from pprint import pprint
from collections import defaultdict

class Node:
    def __init__(self, val, last, position):
        self.id = val
        self.last = last
        self.position = position

words = list()
index = dict()
word_context = defaultdict(dict)
context_word = defaultdict(dict)
word_candidate = dict()

def gen_context(wd):
    for i in range(len(wd)):
        base = wd[ :i] + wd[i+1: ]
        if i not in word_context[wd]:
            word_context[wd][i] = list()
        word_context[wd][i].append(base)
        if i not in context_word[base]:
            context_word[base][i] = set()
        context_word[base][i].add(wd)   

def readfile():
    with open("dictionary.txt") as f:
        for wd in f.read().split():
            wd = wd.upper()
            words.append(wd)
            index[wd] = len(words) - 1            
            gen_context(wd)            

def build_candidates(word):
    cand = [None] * len(word)
    for i in range(len(word)):
        cand[i] = list()
        for base in word_context[word][i]:
            for new_word in context_word[base][i]:
                if new_word != word:
                    cand[i].append(new_word)
    return cand

def chain_ladder(node, depth):
    ladders = [None] * depth
    i = depth - 1
    It = node
    while It:
        ladders[i] = (It.id)
        i -= 1
        It = It.last
    return ladders

def word_ladder(s1, s2):    
    s1 = s1.upper()
    s2 = s2.upper()
    readfile()
    if len(s1) != len(s2) or not len(s1) or s1 not in index or s2 not in index:
        return list()
    if s1 == s2:
        return [[s1]]
    cand_dict = dict()
    chains = list()
    root = Node(s1, None, None)
    level = [root]
    depth = 1
    while not len(chains):
        level = bfs(level, s2, chains, cand_dict)
        depth += 1
    ladders = list()
    for chain in chains:
        ladders.append(chain_ladder(chain, depth))
    return ladders

def bfs(level, target, chains, cand_dict):
    new_level = list()
    for nd in level:
        wd = nd.id
        if wd not in cand_dict:
            cand_dict[wd] = build_candidates(wd)
        for i in range(len(target)):
            if i != nd.position:
                for cand in cand_dict[wd][i]:
                    new_node = Node(cand, nd, i)
                    if cand == target:
                        chains.append(new_node)
                    new_level.append(new_node)
    return new_level

if __name__ == "__main__":
    s = input("Input words: ").split()
    for lst in word_ladder(s[0], s[1]):
        print(lst)

    
                    
    
    
                
                        
