import bz2
import xml.etree.ElementTree as ET
import re
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
        categories=[]
        outEdges=[]
        pageLines=[]
        while line!="</page>":
            pageLines.append(line)
            line=str(bzFile.readline(),'utf-8').strip()
        pageLines.append(line)
        pageRoot = ET.fromstring("\n".join(i for i in pageLines))
        for child in pageRoot:
            for nextchild in child:
                if nextchild.tag=='text':
                    listOfLinks=re.findall('\[\[([^\[\]]*)\]\]',nextchild.text)
                    for link in listOfLinks:
                        link=str(link.split('|')[0])
                        if link.startswith('Category'):
                            categories.append(link[9:])
                        else:
                            if ':' not in link:
                                outEdges.append(link)
        print(outEdges[:10])
        print(categories[:10])
        if c>1:
            break
        c+=1
print(c)