from collections import defaultdict


def read_file():
    words=defaultdict()
    with open("dictionary.txt") as f:
        s = f.read().split('\n')
        for ss in s:
            if len(ss) > maxlen:
                maxlen = len(ss)
