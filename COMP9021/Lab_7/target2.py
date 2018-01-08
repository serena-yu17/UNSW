import sys
from random import choice, sample
from itertools import permutations

class Target:
    def __init__(self, dictionary = "dictionary.txt", target=None, minimal_length=4):
        self.min_len = minimal_length
        self.words = set()
        self.words9set = set()
        words9 = list()
        try:
            with open(dictionary) as f:
                for wd in f.read().split():
                    if len(wd) < 10 and len(wd) == len(set(wd)):
                        wd = wd.upper()
                        self.words.add(wd)
                        wdset = set(wd)
                        if len(wd) == 9:
                            words9.append(wd)
                            self.words9set.add(tuple(sorted(wd)))
        except IOError:
            print("Failed to open file, giving up.")
            sys.exit()
        self.solutions = [None] * 10
        for i in range(10):
            self.solutions[i] = set()
        self.found = 0
        if target is not None:            
            if not isinstance(target, str) or len(target) != 9 or len(set(target)) != 9 or tuple(sorted(target)) not in self.words9set:
                target = None
            else:
                self.target = target
        if not target:
            self.candidate = choice(words9)
            self.target = ''.join(sample(self.candidate, 9))
        self.find_words()

    def __str__(self):
        result = list()
        result.append("       ")
        result.append("___________\n\n")
        for i in range(3):
            result.append("      ")
            result.append("|")
            for j in range(3):
                result.append(" {} |".format(self.target[i * 3 + j]))
            result.append("\n")
            result.append("       ")
            result.append("___________\n\n")
        return ''.join(result)

    def __repr__(self):
        return str(self)

    def number_of_solutions(self):
        print("In decreasing order of length between 9 and {}:".format(self.min_len))
        for leng in range(9, -1, -1):
            if len(self.solutions[leng]):
                print("    {} solution of length {}".format(len(self.solutions[leng]), leng))

    def give_solutions(self, minimal_length=None):        
        if minimal_length is None:
            minimal_length = 0        
        for i in range(9, minimal_length - 1, -1):
            if len(self.solutions[i]):
                print("Solution of length {}:".format(i))
                for wd in sorted(self.solutions[i]):
                    print("    {}".format(wd))
                print()

    def find_words(self):
        mid = self.target[4]
        letters = set(self.target)
        for word in self.words:
            wordset = set(word)
            if wordset <= letters and mid in wordset and len(word) >= self.min_len:
                self.solutions[len(word)].add(word)
        
    def change_target(self, st1, st2):
        dic1 = dict()
        for i in range(len(st1)):
            dic1[st1[i]] = i
        set1 = set(dic1)
        set2 = set(st2)
        if len(st1) != len(st2) or not (set1 <= set(self.target)) or len(set1) != len(st1) or len(set2) != len(st2) or\
           (set1 == set2 and self.target[4] not in set1):
            print("The target is not changed.")
            return
        new_target = list()
        for i in range(9):
            if self.target[i] in dic1:
                new_target.append(st2[dic1[self.target[i]]])
            else:
                new_target.append(self.target[i])
        if len(set(new_target)) != len(new_target) or tuple(sorted(new_target)) not in self.words9set:
            print("The target is not changed.")
            return
        self.target = new_target
        for i in range(10):
            self.solutions[i].clear()
        self.find_words()
            




















        
        
                
        
                
                
        
