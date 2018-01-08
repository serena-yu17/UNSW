import sys

s = input("Input the desired size: ")
try:
    size = int(s)
except ValueError:
    print("Invalid value, giving up...")
    sys.exit()
if size <= 0:
    print("Invalid value, giving up...")
    sys.exit()
triangle = [None] * (size + 3)
for i in range(size + 3):
    triangle[i] = [0] * (size + 1)
triangle[1][0] = 1
for y in range(1, size + 1):
    for x in range(y + 1):
        triangle[x + 1][y] = triangle[x][y - 1] + triangle[x + 2][y - 1]
    triangle[0][y] = triangle[2][y]
lines = list()
lines.append(r'\documentclass[10pt]{article}' + '\n')
lines.append(r'\usepackage{tikz}' + '\n')
lines.append(r'\pagestyle{empty}' + '\n')
lines.append(r'\begin{document}' + '\n')
lines.append(r'\vspace*{\fill}' + '\n')
lines.append(r'\begin{center}' + '\n')
lines.append(r'\begin{tikzpicture}[scale=0.047]' + '\n')
for y in range(size + 1):
    for x in range(1, y + 2):
        if triangle[x][y] == 0:
            print(' ', end='')
        else:
            print(triangle[x][y], end='')
    print()

for y in range(size + 1):
    for x in range(1, y + 2):
        if triangle[x][y] & 1 == 1:
            lines.append(f"\\fill({x-1},{-y * 2}) rectangle({x+1},{2-y * 2});\n")
            if x != 1:
                lines.append(f"\\fill({1-x},{-y * 2}) rectangle({3-x},{2-y * 2});\n")
with open("Sierpinski_triangle.tex", 'w') as f:
    f.writelines(lines)
