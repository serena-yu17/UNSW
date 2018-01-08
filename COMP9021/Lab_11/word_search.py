import sys
from collections import defaultdict


class WordSearch:
    def __init__(self, path):
        self.grid = list()
        self.lower_grid = list()
        with open(path) as f:
            for line in f:
                if isinstance(line, str):
                    lst = list()
                    lst_lower = list()
                    for ch in line:
                        if ord(ch) >= ord('A') and ord(ch) <= ord('Z'):
                            lst.append(ch)
                            lst_lower.append(ch.lower())
                    if len(self.grid) > 0 and len(lst) != len(self.grid[-1]):
                        print("Invalid square.")
                        sys.exit(1)
                    self.grid.append(lst)
                    self.lower_grid.append((lst_lower))
        self.size = len(self.grid)
        self.first_letters = defaultdict(list)
        self.buildDict()
        self.solutions = dict()
        self.directions = dict()

    def buildDict(self):
        for y in range(self.size):
            for x in range(self.size):
                self.first_letters[self.grid[y][x]].append((y, x))

    def __str__(self):
        lines = list()
        for y in range(self.size):
            for x in range(self.size):
                if x:
                    lines.append(' ')
                lines.append(self.grid[y][x])
            lines.append('\n')
        return ''.join(lines)

    def number_of_solutions(self, length):
        if length > self.size // 2:
            return 0
        num = self.size * self.size
        num -= self.size * (self.size - length - 1) * 2
        num += (self.size - length - 1) * (self.size - length - 1)
        return num

    def search_direction(self, coord, word, direction):
        dirY, dirX = direction
        y0, x0 = coord
        for i in range(len(word)):
            if y0 < 0 or x0 < 0 or y0 >= self.size or x0 >= self.size or self.grid[y0][x0] != word[i]:
                return 0
            y0 += dirY
            x0 += dirX
        return 1

    def search(self, coord, word):
        if self.search_direction(coord, word, (-1, 0)):
            return (-1, 0), "N"
        if self.search_direction(coord, word, (-1, 1)):
            return (-1, 1), "NE"
        if self.search_direction(coord, word, (0, 1)):
            return (0, 1), "E"
        if self.search_direction(coord, word, (1, 1)):
            return (1, 1), "SE"
        if self.search_direction(coord, word, (1, 0)):
            return (1, 0), "S"
        if self.search_direction(coord, word, (1, -1)):
            return (1, -1), "SW"
        if self.search_direction(coord, word, (0, -1)):
            return (0, -1), "W"
        if self.search_direction(coord, word, (-1, -1)):
            return (-1, -1), "NW"
        else:
            return None

    def find_solution(self, word):
        for coord in sorted(self.first_letters[word[0]]):
            direction = self.search(coord, word)
            if direction:
                self.directions[word] = direction[0]
                self.solutions[word] = (coord[1], coord[0], direction[1])
                return
        self.solutions[word] = None
        self.directions[word] = None

    def locate_words_in_grid(self, *args):
        for word in args:
            self.find_solution(word)
        return self.solutions

    def display_word_in_grid(self, word):
        if self.solutions[word]:
            y0 = self.solutions[word][1]
            x0 = self.solutions[word][0]
            direction = self.directions[word]
            letters = set()
            for i in range(len(word)):
                letters.add((y0, x0))
                y0 += direction[0]
                x0 += direction[1]
            for y in range(self.size):
                for x in range(self.size):
                    if x:
                        print(' ', end='')
                    if (y, x) in letters:
                        print(self.grid[y][x], end='')
                    else:
                        print(self.lower_grid[y][x], end='')
                print()


if __name__ == "__main__":
    import pprint

    ws = WordSearch("word_search_1.txt")
    print(ws)
    metals = (
        "PLATINUM", "COPPER", "MERCURY", "TUNGSTEN", "MAGNESIUM", "ZINC", "MANGANESE", "TITANIUM", "TIN", "IRON",
        "LITHIUM",
        "CADMIUM", "GOLD", "COBALT", "SILVER", "NICKEL", "LEAD", "IRIDIUM", "URANIUM", "SODIUM")
    located_metals = ws.locate_words_in_grid(*metals)
    pprint.pprint(located_metals)
    for metal in metals:
        print(metal, end=':\n')
        ws.display_word_in_grid(metal)
        print()
