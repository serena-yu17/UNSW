def getp(num):
    pat=[]
    while num!=0:
        pat.append((num%10)&1)
        num=num//10
    pat.reverse()
    return pat

i=100
found=0
while i<988 and found==0:
    if getp(i) == [1,0,0]:
        j=20
        while j<88 and found==0:
            if getp(j) == [0,0]:
                mult1=i*(j%10)
                if getp(mult1)==[0,1,0,0]:
                    mult2=i*(j//10)
                    if getp(mult2)==[0,1,0]:
                           mult3=i*j
                           if getp(mult3)==[1,1,0,0]:
                               found=1
                               print("", i)
                               print("x", j)
                               print("-----")
                               print(mult1)
                               print(mult2)
                               print("-----")
                               print(mult3)
                               break
            j+=1
    i+=1
