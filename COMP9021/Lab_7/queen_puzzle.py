from time import time


class QueenPuzzle:
    def __init__(self, size):
        self.size = size
        self.n_test = 0
        self.solutions = list()
        self.lst = list(range(self.size))
        time1 = time()
        self.search()
        print("time elapsed:", time() - time1)

    def check(self, grid):
        for i in range(self.size - 1):
            for j in range(i + 1, self.size):
                if abs(i - j) == abs(grid[i] - grid[j]):
                    return j
        return 0

    def search(self):
        while self.perm(self.lst):
            self.skip()
            self.n_test += 1
            if not self.check(self.lst):
                self.solutions.append(self.lst.copy())

    @staticmethod
    def rev(lst, begin, end):
        while begin < end:
            lst[begin], lst[end] = lst[end], lst[begin]
            begin += 1
            end -= 1

    def perm(self, lst):
        leng = len(lst)
        i = leng - 1
        while 1:
            j = i
            i -= 1
            if lst[i] < lst[j]:
                k = leng
                while lst[i] >= lst[k - 1]:
                    k -= 1
                k -= 1
                lst[i], lst[k] = lst[k], lst[i]
                self.rev(lst, j, leng - 1)
                return 1
            if i == 0:
                lst.reverse()
                return 0

    @staticmethod
    def can_skip(lst, i):
        for j in range(i - 1, -1, -1):
            if abs(i - j) == abs(lst[i] - lst[j]):
                return 1
        return 0

    def skip(self):
        found = 1
        while found:
            found = 0
            i = 0
            while i < self.size - 1 and not (self.can_skip(self.lst, i) and self.lst[i] < self.lst[i + 1]):
                i += 1
            if i != 0:
                found = 1
            lower = sorted(self.lst[i:])
            nxt = 0
            for n in lower:
                if n > self.lst[i]:
                    nxt = n
                    break
            if nxt == 0:
                return
            else:
                # self.lst = self.lst[:i] + [nxt] + (sorted(self.lst[i:])-[nxt])
                self.lst[i] = nxt
                p_lst = i + 1
                p_lower = 0
                while p_lst < self.size:
                    if lower[p_lower] != nxt:
                        self.lst[p_lst] = lower[p_lower]
                        p_lst += 1
                    p_lower += 1

    def print_nb_of_tested_permutations(self):
        print(self.n_test)

    def print_nb_of_solutions(self):
        print(len(self.solutions))

    def print_solution(self, n):
        if n < len(self.solutions):
            tup = self.solutions[n]
            lines = []
            for y in range(self.size):
                line = []
                for x in range(self.size):
                    if x != tup[y]:
                        line.append('0')
                    else:
                        line.append('1')
                line = ' '.join(line)
                lines.append(line)
            lines = '\n'.join(lines)
            print(lines)


if __name__ == "__main__":
    puzzle = QueenPuzzle(8)
    puzzle.print_nb_of_tested_permutations()
    puzzle.print_nb_of_solutions()
