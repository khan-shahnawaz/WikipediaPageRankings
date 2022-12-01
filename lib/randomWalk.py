import random
from .createWikiGraph import WikiGraphCreator
import heapq

class RandomWalk():
    def __init__(self, graph:WikiGraphCreator) -> None:
        self.helperFileName = graph.helperFileName
        self.offsetMap = {}
        self.nodeList={}
        self.numNodes=0
        self.numVisits=[]
    def loadGraph(self) -> None:
        with open(self.helperFileName, 'r', encoding='utf-8') as f:
            curLine = f.readline()
            while curLine:
                nodeName = curLine.strip()
                self.nodeList[self.numNodes]= nodeName
                
                curLine = f.readline()
                categoryOffset, outlinkOffset = curLine.strip().split(' ')
                self.offsetMap[self.numNodes] = (int(categoryOffset), int(outlinkOffset))
                self.numNodes+=1
                curLine = f.readline()
    def randomWalk(self, startNode:str, numSteps:int) -> list:
        path = [startNode]
        for i in range(numSteps):
            with open(self.helperFileName, 'r', encoding='utf-8') as f:
                f.seek(self.offsetMap[startNode][1])
                numOutLinks = int(f.readline().strip())
                outLinks = []
                for i in range(numOutLinks):
                    outLinks.append(f.readline().strip())
                startNode = random.choice(outLinks)
                path.append(startNode)
        return path