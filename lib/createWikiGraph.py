import bz2
import xml.etree.ElementTree as ET
import re

class WikiGraphCreator():
    def __init__(self, dumpFileName:str, graphFileName:str)->None:
        self.bzFiile = bz2.BZ2File(dumpFileName)
        self.graphFile = open(graphFileName,'w',encoding='utf-8')
        self.totalTime=0
        self.completed=False













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
            if child.tag=='title':
                title=child.text
            for nextchild in child:
                if nextchild.tag=='text':
                    listOfLinks=re.findall('\[\[([^\[\]]+)\]\]',nextchild.text)
                    for link in listOfLinks:
                        link=str(link.split('|')[0])
                        if link.startswith('Category:'):
                            categories.append(link[9:])
                        else:
                            if ':' not in link:
                                outEdges.append(link)
        
        graphFile.write(title)
        graphFile.write('\n')
        graphFile.write(str(len(categories)))
        graphFile.write('\n')
        for category in categories:
            graphFile.write(category)
            graphFile.write('\n')
        graphFile.write(str(len(outEdges)))
        graphFile.write('\n')
        for outEdge in outEdges:
            graphFile.write(outEdge)
            graphFile.write('\n')
        c+=1
print(c)