from math import log10


def seek(cur_sum, note, used_notes, count):
    global solution
    global max_count
    used_notes[note] += 1
    count += 1
    cur_sum += notes[note]
    if cur_sum == target:
        if solution is None or count < max_count:
            solution = used_notes
            max_count = count
    elif cur_sum < target and (solution is None or count < max_count):
        for i in range(len(notes) - 1, -1, -1):
            seek(cur_sum, i, used_notes.copy(), count)


s = input("Input the desired amount: ")
target = 0
try:
    target = int(s)
    if target < 0:
        raise ValueError
except ValueError:
    print("Invalid input, giving up...")
notes = [1, 2, 5, 10, 20, 50, 100]
used_notes = [0] * 7
solution = None
hundred = target // 100
used_notes[-1] = hundred
max_count = hundred
for i in range(len(notes) - 1, -1, -1):
    seek(hundred * 100, i, used_notes.copy(), hundred)
if max_count == 1:
    pl = "banknote"
else:
    pl = "banknotes"
print("\n{} {} is needed.".format(max_count, pl))
print("The detail is:")
leng = 1
for i in range(len(solution)):
    if int(log10(notes[i]) + 1) > leng:
        leng = int(log10(notes[i]) + 1)
for i in range(len(solution) - 1, -1, -1):
    if solution[i] != 0:
        print(' ' * (leng-int(log10(notes[i]) + 1)), end="")
        print("${}: {}".format(notes[i], solution[i]))
