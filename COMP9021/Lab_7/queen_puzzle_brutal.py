from time import time


def rev(tup):
    lst = list(tup)
    lst.reverse()
    return lst


class QueenPuzzle:
    def __init__(self, size):
        self.size = size
        self.n_test = 0
        self.solutions = list()
        time1 = time()
        self.search()
        print("time elapsed:", time() - time1)
        '''for tup in sorted(self.solutions, key=rev, reverse=True):
            print(tup)'''

    def check(self, grid):
        for i in range(self.size - 1):
            for j in range(i + 1, self.size):
                if abs(i - j) == abs(grid[i] - grid[j]):
                    return 0
        return 1

    def search(self):
        lst=list(range(self.size))
        while self.perm(lst):
            self.n_test += 1
            if self.check(lst):
                self.solutions.append(lst)
                print(lst)

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
