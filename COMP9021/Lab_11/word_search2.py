from collections import defaultdict

class WordSearchException(Exception):
    def __init__(self, message):
        self.message = message

class WordSearch:
    def __init__(self, file_path):
        self.grid = list()
        self.letters = defaultdict(list)
        y = 0        
        with open(file_path) as f:            
            for lineStr in f.read().split('\n'):
                line = list()
                x = 0
                lineStr = lineStr.strip()
                for ch in lineStr:
                    if ch >= 'A' and ch <= 'Z':
                        line.append(ch)
                        self.letters[ch].append((y,x))
                        x += 1
                if len(line):
                    self.grid.append(line)
                    y += 1
        self.size = len(self.grid)
        self.directions = {'N':(-1, 0), 'NE':(-1, 1), 'E':(0,1), 'SE':(1,1),
                           'S':(1,0), 'SW':(1,-1), 'W':(0,-1), 'NW':(-1,-1)}

    def __str__(self):
        lines = list()
        for y in range(self.size):
            for x in range(len(self.grid[y])):
                if x:
                    lines.append(' ')
                lines.append(self.grid[y][x])
            if y != self.size -1:    
                lines.append('\n')
        lines = ''.join(lines)
        return lines

    def __repr__(self):
        return str(self)
    
    def number_of_solutions(self, length):
        return 2 * (self.size * (self.size - length -1)) + 2 * (
            (self.size - length -1) * (self.size - length -1))

    def search(self, word, coord):
        y0, x0 = coord        
        for key in self.directions:
            found = 1
            direction = self.directions[key]            
            for i in range(1, len(word)):
                if y0 + direction[0] * i >= self.size or x0 + direction[1] * i >= self.size \
                   or self.grid[y0 + direction[0] * i][x0 + direction[1] * i] != word[i]:
                    found = 0
                    break
            if (found):
                return (x0, y0, key)
        return None
            
    def locate_word_in_grid(self, word):
        word.upper()
        coordinates = self.letters[word[0]]
        for coord in coordinates:
             found = self.search(word, coord)
             if (found):
                 return found
        return None

    
    def locate_words_in_grid(self, *words):
        result = dict()
        for wd in words:
            result[wd] = self.locate_word_in_grid(wd)
        return result

    def display_word_in_grid(self, word):
        found = self.locate_word_in_grid(word)
        if (found):
            x0, y0, direc = found
            direction = self.directions[direc]
            coords = set()
            for i in range(len(word)):
                coords.add((y0 + i * direction[0], x0 + i * direction[1]))
            for y in range(self.size):
                for x in range(len(self.grid[y])):                
                    if x:
                        print(' ', end='')
                    ch = self.grid[y][x]
                    if (y,x) in coords:
                        print(ch, end='')
                    else:
                        print(ch.lower(), end='')
                print()
                    

    









        
        
