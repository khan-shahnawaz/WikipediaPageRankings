import bz2
import xml.etree.ElementTree as ET
import re
import time

#Class that creates wikigraph file
class WikiGraphCreator():
    def __init__(self, dumpFileLocation:str, graphFileLocation:str)->None:
        ''' Constructor to Open files and initialise variables'''
        
        self.bzFile = bz2.BZ2File(dumpFileLocation)
        self.graphFile = open(graphFileLocation,'w',encoding='utf-8')
        self.dumpFileName=dumpFileLocation
        self.graphFileName=graphFileLocation
        self.totalTime=0
        self.completed=False
        self.totalNodes=0
        self.totalEdges=0
        self.totalCategories=0      #Stores sum of all categories marked for all nodes
        
    def createGraph(self)->None:
        ''' Creates wikigraph for the object '''
        startTime=time.time()
        
        while True:
            nextLine=self.bzFile.readline()
            if not nextLine:
                ''' Break if EOF detected '''
                break
            
            line=str(nextLine, 'utf-8').strip()
            if line=="<page>":
                
                ''' If a new page starts'''
                categories=[]
                outEdges=[]
                pageLines=[]
                self.totalNodes+=1
                while line!="</page>":
                    pageLines.append(line)
                    line=str(self.bzFile.readline(),'utf-8').strip()
                    
                pageLines.append(line)
                pageRoot = ET.fromstring("\n".join(i for i in pageLines))   #Creates XML Trees
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
                                    self.totalCategories+=1
                                else:
                                    if ':' not in link:
                                        outEdges.append(link)
                                        self.totalEdges+=1
                
                self.graphFile.write(title)
                self.graphFile.write('\n')
                self.graphFile.write(str(len(categories)))
                self.graphFile.write('\n')
                for category in categories:
                    self.graphFile.write(category)
                    self.graphFile.write('\n')
                self.graphFile.write(str(len(outEdges)))
                self.graphFile.write('\n')
                for outEdge in outEdges:
                    self.graphFile.write(outEdge)
                    self.graphFile.write('\n')
        endTime=time.time()
        self.totalTime=(endTime-startTime)
        self.completed=True
    def printStatistics(self)->None:
        print("WikiGraph created from dump {} and stored in {}".format(self.dumpFileName, self.graphFileName))
        print("Total Time Taken:",self.totalTime,'seconds')
        print("Number of Pages:", self.totalNodes)
        print("Number of outLinks:", self.totalEdges)
        print("Total Number of Categories(with duplicates) across all pages:",self.totalCategories)
        return