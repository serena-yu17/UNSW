from collections import defaultdict
from random import sample
from itertools import permutations


class Target:
    def __init__(self, dictionary="dictionary.txt", target=None, minimal_length=4):
        if minimal_length < 0:
            minimal_length = 0
        if minimal_length > 9:
            minimal_length = 9
        self.min_length = minimal_length

        self.dictionary = dictionary
        self.words9 = set()
        self.allwords = set()
        with open(self.dictionary) as f:
            s = f.read().split("\n")
            for st in s:
                if isinstance(st, str) and len(st) >= self.min_length:
                    self.allwords.add(st)
                    st_set = set()
                    if len(st) == 9:
                        for ch in st:
                            st_set.add(ch)
                        if len(st_set) == 9:
                            self.words9.add(tuple(sorted(st)))

        self.target = target
        if target is not None and len(target) == 9:
            set_t = set()
            self.target = []
            for i in range(len(target)):
                if ord(target[i]) < ord('A') or ord(target[i]) > ord('Z'):
                    self.target = None
                    break
                set_t.add(target[i])
                self.target.append(target[i])
            if len(set_t) != len(self.target):
                self.target = None
            if tuple(sorted(self.target)) not in self.words9:
                self.target = None

        if self.target is None:
            source = sample(self.words9, 1)[0]
            perm = list(permutations(source, 9))
            self.target = list(sample(perm, 1)[0])

        self.comb = self.seek(self, self.target)

    def __repr__(self):
        return f"Target(dictionary = {self.dictionary}, minimal_length = {self.min_length}"

    def __str__(self):
        grid = [None] * 3
        for x in range(3):
            grid[x] = [self.target[i + x * 3] for i in range(3)]
        st = []
        st.append("\n       ___________\n\n")
        for y in range(3):
            st.append("      |")
            for x in range(3):
                st.append(f" {grid[y][x]} |")
            if y != 2:
                st.append("\n       ___________\n\n")
            else:
                st.append("\n       ___________\n")
        st = "".join(st)
        return st

    def number_of_solutions(self):
        print(f"In decreasing order of length between 9 and {self.min_length}:")
        for leng in sorted(self.comb, reverse=True):
            len_solution = len(self.comb[leng])
            if len_solution == 1:
                sol = "solution"
            else:
                sol = "solutions"
            print(f"    {len_solution} {sol} of length {leng}")

    def give_solutions(self, minimal_length=None):
        if minimal_length is None:
            minimal_length = self.min_length
        for leng in range(9, minimal_length - 1, -1):
            if len(self.comb[leng]) > 0:
                len_solution = len(self.comb[leng])
                if len_solution == 1:
                    sol = "Solution"
                else:
                    sol = "Solutions"
                print(f"{sol} of length {leng}:")
                for s in sorted(self.comb[leng]):
                    print("    ", end="")
                    print(s)
                if leng != minimal_length:
                    print()

    def change_target(self, str_origin, str_change):
        if str_origin == str_change:
            print("The target was not changed.")
            return
        if len(str_origin) != len(str_change):
            print("The target was not changed.")
            return
        arr_origin = []
        set_origin = set()
        arr_change = []
        set_change = set()
        for ch in str_origin:
            arr_origin.append(ch)
            set_origin.add(ch)
        for ch in str_change:
            if ord(ch) < ord('A') or ord(ch) > ord('Z'):
                print("The target was not changed.")
                return
            arr_change.append(ch)
            set_change.add(ch)
        if len(set_change) != len(arr_change) or len(set_change) != len(set_origin) \
                or len(set_origin) != len(arr_origin) or not set_origin.issubset(set(self.target)):
            print("The target was not changed.")
            return
        if set_change == set_origin and self.target[4] not in set_change:
            print("The solutions are not changed.")
            return
        tg = self.target.copy()
        elem_id = dict()
        for i in range(9):
            elem_id[tg[i]] = i
        for i in range(len(arr_origin)):
            tg[elem_id[arr_origin[i]]] = arr_change[i]
        tg_set = set(tg)
        if len(tg) != len(tg_set):
            print("The target was not changed.")
            return
        new_comb = self.seek(self, tg)
        if new_comb == self.comb:
            print("The solutions are not changed.")
            return
        if len(new_comb[9]) == 0:
            print("The target was not changed.")
            return
        else:
            self.target = tg
            self.comb = new_comb

    @staticmethod
    def seek(self, target):
        comb = defaultdict(set)
        tg = target.copy()
        tg.remove(tg[4])
        for leng in range(self.min_length - 1, 9):
            perm = permutations(tg, leng)
            count = 0
            for tup in perm:
                for i in range(leng + 1):
                    word = []
                    if i > 0:
                        for e in tup[:i]:
                            word.append(e)
                    word.append(target[4])
                    if i < leng:
                        for e in tup[i:]:
                            word.append(e)
                    word = "".join(word)
                    if word in self.allwords:
                        comb[leng + 1].add(word)
                count += 1
        return comb
