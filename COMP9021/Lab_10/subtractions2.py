def subtractions(tup, target):
    if len(tup) == 0:
        return
    if len(tup) == 1:
        print(tup[0])
        return
    string = list(map(str, tup))
    expr = divide(string)
    for e in expr:
        if eval(e) == target:
            print(''.join(e))


def divide(lst):
    if len(lst) == 1:
        return lst
    expr = list()
    for i in range(1,len(lst)):
        left = divide(lst[:i])
        right = divide(lst[i:])        
        for l in left:
            for r in right:
                expr.append(''.join(['(', l, ' - ', r, ')']))
    return expr
                            
    
