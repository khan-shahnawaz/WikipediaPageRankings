f=open('graph.txt','r', encoding='utf-8')
c=0
for i in f:
    c+=1
    if len(i)==1:
        print("Found")
        print(c)
        break