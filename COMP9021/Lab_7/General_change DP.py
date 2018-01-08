import sys
from math import log10
from collections import defaultdict

# IO
print("Input pairs of the form ’value : number’")
print("   to indicate that you have ’number’ many banknotes of face value ’value’.")
print("Input these pairs one per line, with a blank line to indicate end of input.\n")
s = "dummy"
notes = defaultdict(int)
while 1:
    s = input()
    if s == "":
        break
    s = s.split(":")
    try:
        if len(s) != 2 or not s[0].isdigit or not s[1].isdigit:
            raise ValueError
        note = int(s[0])
        num = int(s[1])
        if note <= 0 or num <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input.")
        sys.exit(1)
    notes[note] = num
if len(notes) == 0:
    print("Invalid input.")
    sys.exit(1)
s = input("Input the desired amount: ")
try:
    total = int(s)
    if total <= 0:
        raise ValueError
except ValueError:
    print("Invalid input.")
    sys.exit(1)
large = 1
for note in notes:
    if note < total:
        large = 0
if large == 1:
    print("There is no solution.")
    sys.exit(0)

# process
min_len = 65535
min_notes = set()

id_notes = dict()
note_id = sorted(notes)
for i in range(len(note_id)):
    id_notes[note_id[i]] = i


def seek(cur_sum, note, used_note):
    global min_len
    global min_notes
    if sum(used_note) >= min_len:
        return
    used_note = used_note.copy()
    if cur_sum + note == total:
        used_note[id_notes[note]] += 1
        if sum(used_note) < min_len:
            min_len = sum(used_note)
            min_notes.clear()
            min_notes.add(tuple(used_note))
        elif sum(used_note) == min_len:
            min_notes.add(tuple(used_note))
        return
    if cur_sum + note < total:
        cur_sum += note
        used_note[id_notes[note]] += 1
        for nt in notes:
            if used_note[id_notes[note]] < notes[nt] - 1:
                seek(cur_sum, nt, used_note)


initial = [0] * len(notes)
for nt in notes:
    seek(0, nt, initial)

if min_len == 65535:
    print("There is no solution.")
    sys.exit(0)
if len(min_notes) > 1:
    print("There are {} solutions:".format(len(min_notes)))
for tup in sorted(min_notes):
    max_index = 0
    max_val = 0
    for i in range(len(tup)):
        if tup[i] != 0:
            max_index = note_id[i]
            if tup[i] > max_val:
                max_val = tup[i]
    len1 = int(log10(max_index))
    len2 = int(log10(max_val))
    for i in range(len(tup)):
        if tup[i] != 0:
            st = list("$")
            st.append(str(note_id[i]))
            st.append(' ' * (len1 - int(log10(note_id[i]))))
            st.append(": ")
            st.append(' ' * (len2 - int(log10(tup[i]))))
            st.append(str((tup[i])))
            print("".join(st))
    print()
