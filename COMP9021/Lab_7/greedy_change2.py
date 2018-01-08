import sys
from collections import defaultdict

s = input("Input the desired amount: ")
try:
    target = int(s)
    if target < 0:
        raise ValueError
except ValueError:
    print("Invalid input, giving up...")
    sys.exit()    
notes = [100, 50, 20, 10, 5, 2, 1]
exchange = [0] * len(notes)
count = 0
i = 0
while i < len(notes) and notes[i] > target:
    i += 1
while i < len(notes) and target:
    exchange[i] = target // notes[i]
    count += exchange[i]
    target = target % notes[i]
    i += 1
print("\n{} banknotes are needed".format(count))
print("The detail is:")
for i in range(len(exchange)):
    if exchange[i]:
        print("${}: {}".format(notes[i], exchange[i]))


    
    
    
      
