import bz2
filename="./DumpFiles/enwiki-latest-pages-articles1.xml-p1p41242.bz2"
outputFileName="./WikiGraph/graph.txt"
graphFile=open(outputFileName,'w',encoding='utf-8')
bzFile = bz2.BZ2File(filename)
c=0
while True:
    nextLine=bzFile.readline()
    if not nextLine:
        break
    line=str(nextLine, 'utf-8').strip()
    if line=="<page>":
        while line!="</page>":
            if line.startswith('<title>'):
                title= line[7:-8]
            nextLine=bzFile.readline()
            line=str(nextLine, 'utf-8').strip()
        
        graphFile.write(title+'\n')
        c+=1
print(c)