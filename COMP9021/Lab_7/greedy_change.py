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
notes = [100, 50, 20, 10, 5, 2, 1]
count = [0] * 7
for i in range(7):
    count[i] = target // notes[i]
    target = target % notes[i]
all_sum = sum(count)
if all_sum == 1:
    pl = "banknote is"
else:
    pl = "banknotes are"
print("\n{} {} needed".format(all_sum, pl))
i = 0
while not count[i]:
    i += 1
leng = int(log10(notes[i])) + 1
for i in range(7):
    if count[i]:
        print(' ' * (leng - int(log10(notes[i])) - 1), end="")
        print("${}: {}".format(notes[i], count[i]))
