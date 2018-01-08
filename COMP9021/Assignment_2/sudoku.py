from collections import defaultdict
from copy import deepcopy


class Sudoku:
    def __init__(self, path):
        if not isinstance(path, str):
            raise self.SudokuError("Incorrect input")
        self.grid = [None] * 9
        for i in range(9):
            self.grid[i] = [None] * 9
        with open(path) as f:
            lines = f.read().split('\n')
            y = 0
            for line in lines:
                line = line.strip()
                if line is not None and len(line) > 0:
                    buffer = []
                    for i in range(len(line)):
                        if line[i].isdigit():
                            buffer.append(int(line[i]))
                    if len(buffer) != 9:
                        raise self.SudokuError("Incorrect input")
                    x = 0
                    for e in buffer:
                        self.grid[x][y] = buffer[x]
                        x += 1
                    if x != 9:
                        raise self.SudokuError("Incorrect input")
                    y += 1
                    buffer.clear()
            if y != 9:
                raise self.SudokuError("Incorrect input")
        i = len(path) - 1
        while path[i] != '.':
            i -= 1
        self.path_name = path[:i]

        self.all_num = set(range(1, 10))  # all usable numbers

        self.bare = deepcopy(self.grid)  # bare grid, for printing

        self.marks = [None] * 9  # candidates
        for i in range(9):
            self.marks[i] = [None] * 9
            for j in range(9):
                self.marks[i][j] = set()

        self.sizedic = defaultdict(set)

        self.getmark()

        self.preass = self.check()  # also fills candidate numbers

        if self.preass:

            self.force()
            self.forced = deepcopy(self.grid)  # forced, for printing

            self.marks_ini = deepcopy(self.marks)  # initial marks after forced, for printing

            self.work()
            self.crossed = [None] * 9  # crossed marks.
            for i in range(9):
                self.crossed[i] = [None] * 9
                for j in range(9):
                    self.crossed[i][j] = self.marks_ini[i][j] - self.marks[i][j]
        pass

    ##########
    def work(self):
        self.force_cross()
        while self.find_preem():
            pass

    # 0 - row, 1 - col, 2 - box, 3- row box, 4- col box
    def getcoord(self, x0, y0, style):
        if style == 0:
            return self.getcoord_row(y0)
        elif style == 1:
            return self.getcoord_col(x0)
        elif style == 2:
            return self.getcoord_box(x0, y0)
        '''elif style == 3:
            return self.getcoord_row(y0) | self.getcoord_box(x0, y0)
        elif style == 4:
            return self.getcoord_col(x0) | self.getcoord_box(x0, y0)'''

    def getcoord_row(self, y0):
        row = set()
        for x in range(9):
            if self.grid[x][y0] == 0:
                row.add((x, y0))
        return row

    def getcoord_col(self, x0):
        col = set()
        for y in range(9):
            if self.grid[x0][y] == 0:
                col.add((x0, y))
        return col

    def getcoord_box(self, x0, y0):
        box = set()
        x_box = (x0 // 3) * 3
        y_box = (y0 // 3) * 3
        for x in range(3):
            for y in range(3):
                if self.grid[x + x_box][y + y_box] == 0:
                    box.add((x + x_box, y + y_box))
        return box

    def rec_search(self, preem, style_coord, style, next_pt, used, all_preem):
        preem |= self.marks[next_pt[0]][next_pt[1]]
        used.add(next_pt)
        count = 0
        for tup in style_coord:
            if self.marks[tup[0]][tup[1]] <= preem:
                count += 1
                if style > 2 and count > 3:
                    return
        if count == len(preem) and len(preem) <= len(style_coord):
            if preem not in all_preem:
                all_preem.append(preem)
            return
        elif count < len(preem):
            for pt in style_coord - used:
                self.rec_search(preem.copy(), style_coord, style, pt, used.copy(), all_preem)



                # Style: 0 - row, 1 - col, 2 - box, 3- row box, 4- col box

    def search_pm(self, style_coord, style):
        all_preem = list()
        found = 0
        for next_pt in style_coord:
            preem = set()
            used = set()
            self.rec_search(preem, style_coord, style, next_pt, used, all_preem)
        if len(all_preem) == 0:
            return 0
        else:
            for preem in all_preem:
                for pt in style_coord:
                    x, y = pt
                    if not (self.marks[x][y] <= preem):
                        for n in self.marks[x][y].copy():
                            if n in preem:
                                # self.crossed[x][y].add(n)
                                self.sizedic[len(self.marks[x][y])].remove(pt)
                                self.marks[x][y].remove(n)
                                self.sizedic[len(self.marks[x][y])].add(pt)
                                found = 1
            if found == 1:
                self.force_cross()
            return found

    def find_preem(self):
        found = 0
        for style in range(3):
            if style == 0:  # row
                for y in range(9):
                    style_coord = self.getcoord(0, y, style)
                    if self.search_pm(style_coord, style):
                        found = 1
            elif style == 1:
                for x in range(9):
                    style_coord = self.getcoord(x, 0, style)
                    if self.search_pm(style_coord, style):
                        found = 1
            elif style == 2:
                for x in range(3):
                    for y in range(3):
                        style_coord = self.getcoord(x * 3, y * 3, style)
                        if self.search_pm(style_coord, style):
                            found = 1
            '''elif style > 2:  # row box or col box
                for y in range(9):
                    for x in range(9):
                        if self.grid[x][y] == 0:
                            style_coord = self.getcoord(x, y, style)
                            if self.search_pm(style_coord, style):
                                found = 1'''
        return found

    def getmark(self):
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    self.marks[x][y] = self.all_num.difference(
                        set(self.getbox(self.grid, x, y)), set(self.getrow(self.grid, y)),
                        set(self.getcolumn(self.grid, x)), {0})
                    self.sizedic[len(self.marks[x][y])].add((x, y))
                else:
                    if len(self.marks[x][y]) > 0:
                        self.sizedic[len(self.marks[x][y])].remove((x, y))
                        self.marks[x][y].clear()

    def updmark(self):
        for size in range(8, 0, -1):
            for tup in self.sizedic[size].copy():
                x, y = tup
                if self.grid[x][y] == 0:
                    new_mark = self.marks[x][y].difference(
                        set(self.getbox(self.grid, x, y)), set(self.getrow(self.grid, y)),
                        set(self.getcolumn(self.grid, x)), {0})
                    if size != len(new_mark):
                        # self.crossed[x][y] |= self.marks[x][y] - new_mark
                        self.sizedic[size].remove(tup)
                        self.sizedic[len(new_mark)].add(tup)
                        self.marks[x][y] = new_mark
                else:
                    self.sizedic[size].remove(tup)
                    # self.crossed[x][y] |= self.marks[x][y]
                    self.marks[x][y].clear()

    ##############

    @staticmethod
    def checkunit(lst):
        dic = defaultdict(int)
        if isinstance(lst[0], int):
            for e in lst:
                if e != 0:
                    dic[e] += 1
                    if dic[e] > 1:  # repeat
                        return 0
        return 1

    def check(self):
        for x in range(9):
            if not self.checkunit(self.getrow(self.grid, x)):
                return 0
            if not self.checkunit(self.getcolumn(self.grid, x)):
                return 0
        for x in range(3):
            for y in range(3):
                if not self.checkunit(self.getbox(self.grid, x * 3, y * 3)):
                    return 0
        for y in range(9):
            for x in range(9):
                if self.grid[x][y] == 0 and len(self.marks[x][y]) == 0:
                    return 0
        return 1

    def preassess(self):
        if not self.preass:
            print("There is clearly no solution.")
        else:
            print("There might be a solution.")

    #############
    @staticmethod
    def getdic(lst):
        count = defaultdict(int)
        for s_set in lst:
            if len(s_set) > 0:
                for n in s_set:
                    count[n] += 1
        return count

    def force(self):
        box_count = [None] * 3
        for i in range(3):
            box_count[i] = [None] * 3
            for j in range(3):
                box_count[i][j] = set()
        found = 2  # dummy
        while found:
            for x in range(3):
                for y in range(3):
                    box_count[x][y] = self.getdic(self.getbox(self.marks, x * 3, y * 3))
            found = 0
            for x in range(9):
                for y in range(9):
                    if len(self.marks[x][y]) == 1:
                        self.grid[x][y] = next(iter(self.marks[x][y]))
                        found = 1
                        break
                    elif len(self.marks[x][y]) > 1:
                        for n in self.marks[x][y]:
                            if box_count[x // 3][y // 3][n] == 1:
                                found = 1
                                self.grid[x][y] = n
                                break
            if found:
                self.getmark()

    def force_cross(self):
        self.updmark()
        box_count = [None] * 3
        for i in range(3):
            box_count[i] = [None] * 3
            for j in range(3):
                box_count[i][j] = set()
        row_count = [None] * 9
        col_count = [None] * 9
        found = 1  # dummy
        while found:
            found = 0
            for x in range(3):
                for y in range(3):
                    box_count[x][y] = self.getdic(self.getbox(self.marks, x * 3, y * 3))
            for i in range(9):
                row_count[i] = self.getdic(self.getrow(self.marks, i))
                col_count[i] = self.getdic(self.getcolumn(self.marks, i))
            while self.force_cross_cycle(row_count, col_count, box_count):
                found = 1

    # using "return" can save a lot of effort exiting multiple cycles
    def force_cross_cycle(self, row_count, col_count, box_count):
        for size in self.sizedic:
            for tup in self.sizedic[size]:
                x, y = tup
                if len(self.marks[x][y]) == 1:
                    n = next(iter(self.marks[x][y]))
                    self.grid[x][y] = n
                    self.updmark()
                    return 1
                elif len(self.marks[x][y]) > 1:
                    for n in self.marks[x][y]:
                        if box_count[x // 3][y // 3][n] == 1 or row_count[y][n] == 1 or col_count[x][n] == 1:
                            self.grid[x][y] = n
                            self.updmark()
                            return 1
        return 0


        ############

    def bare_tex_output(self):
        lines = self.getlatex(self.bare)
        path = self.path_name + "_bare.tex"
        with open(path, 'w') as f:
            f.write(lines)

    def forced_tex_output(self):
        if not self.preass:
            print("There is clearly no solution.")
            return
        lines = self.getlatex(self.forced)
        path = self.path_name + "_forced.tex"
        with open(path, 'w') as f:
            f.write(lines)

    def marked_tex_output(self):
        if not self.preass:
            print("There is clearly no solution.")
            return
        lines = self.getlatex(self.forced, self.marks_ini)
        path = self.path_name + "_marked.tex"
        with open(path, 'w') as f:
            f.write(lines)

    def worked_tex_output(self):
        if not self.preass:
            print("There is clearly no solution.")
            return
        lines = self.getlatex(self.grid, self.marks_ini, self.crossed)
        path = self.path_name + "_worked.tex"
        with open(path, 'w') as f:
            f.write(lines)

    # extract regions
    @staticmethod
    def getbox(grid, x, y):
        x_box = (x // 3) * 3
        y_box = (y // 3) * 3
        box = list()
        for i in range(3):
            for j in range(3):
                box.append(grid[x_box + i][y_box + j])
        return box

    @staticmethod
    def getrow(grid, y):
        row = [None] * 9
        for x in range(9):
            row[x] = grid[x][y]
        return row

    @staticmethod
    def getcolumn(grid, x):
        column = [None] * 9
        for y in range(9):
            column[y] = grid[x][y]
        return column

    # printing
    @staticmethod
    def corners(mark_set, cross_set=None, num=None):
        corn = [None] * 4
        for i in range(4):
            corn[i] = list()
        for n in sorted(mark_set):
            pos = (n - 1) >> 1
            if n == 9:
                pos = 3
            if cross_set is not None and n in cross_set:
                corn[pos].append(r"\cancel{" + str(n) + "}")
            else:
                corn[pos].append(str(n))
        for i in range(4):
            corn[i] = "{" + " ".join(corn[i]) + "}"
        if num is None or num == 0:
            corn.append("{}")
        else:
            corn.append("{")
            corn.append(str(num))
            corn.append("}")
        return r"\N" + "".join(corn)

    def getlatex(self, grid, marks=None, crossed=None):
        lines = [r'\documentclass[10pt]{article}',
                 r'\usepackage[left=0pt,right=0pt]{geometry}',
                 r'\usepackage{tikz}',
                 r'\usetikzlibrary{positioning}',
                 r'\usepackage{cancel}',
                 r'\pagestyle{empty}',
                 '',
                 r'\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},',
                 r'                               label=above right:{\tiny #2},',
                 r'                               label=below left:{\tiny #3},',
                 r'                               label=below right:{\tiny #4}]{#5};}}',
                 '',
                 r'\begin{document}',
                 '',
                 r'\tikzset{every node/.style={minimum size=.5cm}}',
                 '',
                 r'\begin{center}',
                 r'\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline']
        for y in range(9):
            lines.append("% Line {}".format(y + 1))
            line = []
            for x in range(9):
                if grid[x][y] != 0 and crossed is None:
                    line.append(r"\N{}{}{}{}{" + str(grid[x][y]) + "}")

                elif crossed is not None:
                    line.append(self.corners(marks[x][y], crossed[x][y], grid[x][y]))

                elif grid[x][y] == 0 and marks is not None:
                    line.append(self.corners(marks[x][y]))

                else:
                    line.append(r"\N{}{}{}{}{}")

                if x != 8:
                    line.append(r"&")
                if x == 2 or x == 5:
                    lines.append(" ".join(line))
                    line.clear()
                if x == 8:
                    line.append(r"\\ \hline")
                    line = " ".join(line)
                    if y % 3 == 2:
                        line += "\hline"
                    if y != 8:
                        line += '\n'
                    lines.append(line)
                    line = ""
        lines.append(r"\end{tabular}")
        lines.append(r"\end{center}")
        lines.append('')
        lines.append(r"\end{document}" + '\n')
        return "\n".join(lines)

    class SudokuError(Exception):
        def __init__(self, message):
            self.message = message

    # for debug only
    @staticmethod
    def getpreview(grid):
        preview = [None] * len(grid)
        for y in range(len(grid)):
            preview[y] = [None] * len(grid)
            for x in range(len(grid)):
                preview[y][x] = grid[x][y]
        return preview


if __name__ == "__main__":
    sudoku = Sudoku('grid_7.txt')
    s = ""
    while s.lower() != 'q':
        s = input("Input command:\n")
        try:
            eval(s)
        except Sudoku.SudokuError as e:
            print("sudoku.SudokuError:", str(e))
