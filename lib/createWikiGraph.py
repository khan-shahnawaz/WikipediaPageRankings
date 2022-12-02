import bz2
import xml.etree.ElementTree as ET
import re
import time

''' Class that creates wikigraph file'''
class WikiGraphCreator():
    def __init__(self, dumpFileLocation:str, graphFileLocation:str)->None:
        ''' Constructor to Open files and initialise variables'''
        
        
        self.dumpFileName=dumpFileLocation
        self.graphFileName=graphFileLocation
        self.helperFileName = graphFileLocation[:-4]+"_helper.txt"
        self.totalTime=0
        self.completed=False
        self.totalNodes=0
        self.totalEdges=0
        self.totalCategories=0      #Stores sum of all categories marked for all nodes
        
    def createGraph(self)->None:
        ''' Creates wikigraph for the object '''
        self.bzFile = bz2.BZ2File(self.dumpFileName)
        self.graphFile = open(self.graphFileName,'w',encoding='utf-8')
        startTime=time.time()
        
        while True:
            nextLine=self.bzFile.readline()
            if not nextLine:
                ''' Break if EOF detected '''
                break
            
            line=str(nextLine, 'utf-8').strip()
            
            if line=="<page>":
                if self.totalNodes%1000000==0:
                    print("Completed {} Nodes".format(self.totalNodes))
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
                        if '\n' in title:
                            continue
                        self.graphFile.write(title)
                        self.graphFile.write('\n')
                        
                    for nextchild in child:
                        if nextchild.tag=='text':
                            if not nextchild.text:
                                continue    
                            listOfLinks=re.findall('\[\[([^\[\]]+)\]\]',nextchild.text)
                            for link in listOfLinks:
                                link=str(link.split('|')[0])
                                if '\n' in link:
                                    continue
                                if link.startswith('Category:'):
                                    categories.append(link[9:])
                                    self.totalCategories+=1
                                else:
                                    if 'Link:' not in link and 'File:' not in link and 'Wikipedia:' not in link and 'Help:' not in link:
                                        outEdges.append(link)
                                        self.totalEdges+=1
                
                
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
        self.bzFile.close()
        self.graphFile.close()
    
    def createHelperFile(self)->None:
        ''' Creates a helper file for the wikigraph '''
        if not self.completed:
            print("Please create the graph first")
            return
        helperFile=open(self.graphFileName[:-4]+"_helper.txt",'w',encoding='utf-8')
        self.graphFile=open(self.graphFileName,'r',encoding='utf-8')
        c=0
        curLine= self.graphFile.readline()
        while curLine:
            c+=1
            nodeName=curLine.strip()
            
            categoryOffset=self.graphFile.tell()
            numCategory=int(self.graphFile.readline().strip())
            for i in range(numCategory):
                self.graphFile.readline()
            outlinkOffset=self.graphFile.tell()
            numOutLinks=int(self.graphFile.readline().strip())
            for i in range(numOutLinks):
                self.graphFile.readline()
            helperFile.write(nodeName)
            helperFile.write('\n')
            helperFile.write(str(categoryOffset)+' '+str(outlinkOffset)+'\n')
            curLine=self.graphFile.readline()
        helperFile.close()
        self.graphFile.close()
        return
    
    def printStatistics(self)->None:
        print("WikiGraph created from dump {} and stored in {}".format(self.dumpFileName, self.graphFileName))
        print("Total Time Taken:",self.totalTime,'seconds')
        print("Number of Pages:", self.totalNodes)
        print("Number of outLinks:", self.totalEdges)
        print("Total Number of Categories(with duplicates) across all pages:",self.totalCategories)
        return