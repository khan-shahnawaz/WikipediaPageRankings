import random
from .createWikiGraph import WikiGraphCreator
import heapq

class RandomWalk():
    def __init__(self, graph:WikiGraphCreator) -> None:
        self.helperFileName = graph.helperFileName
        self.graphFileName = graph.graphFileName
        self.offsetMap = {}
        self.nodeList={}
        self.numNodes=0
        self.numVisits=[]
        self.nodeIndex={}
        self.walkLength=0
    def loadGraph(self) -> None:
        with open(self.helperFileName, 'r', encoding='utf-8') as f:
            curLine = f.readline()
            while curLine:
                nodeName = curLine.strip()
                self.nodeList[self.numNodes]= nodeName
                self.nodeIndex[nodeName]=self.numNodes
                
                curLine = f.readline()
                categoryOffset, outlinkOffset = curLine.strip().split(' ')
                self.offsetMap[self.numNodes] = (int(categoryOffset), int(outlinkOffset))
                self.numNodes+=1
                curLine = f.readline()
        self.numVisits=[[0,i] for i in range(self.numNodes)]
    def randomWalk(self, startNode: int, walkLength: int) -> None:
        curNode = self.nodeIndex[startNode]
        self.numVisits[curNode][0]-=1
        
        graphFile = open(self.graphFileName, 'r', encoding='utf-8')
        for i in range(walkLength):
            if i%1000==0:
                print("Completed WalkLength of {}".format(i))
            adjacent = []
            categoryOffset, outlinkOffset = self.offsetMap[curNode]
            graphFile.seek(outlinkOffset)
            numNeighbors = int(graphFile.readline().strip())
            for j in range(numNeighbors):
                neighbor = graphFile.readline().strip()
                if neighbor not in self.nodeIndex:
                    continue
                adjacent.append(self.nodeIndex[neighbor])
            teleport= random.randint(1,5)
            if len(adjacent) == 0 or teleport==1:
                curNode = random.randint(0, self.numNodes - 1)
            else:
                curNode=random.choice(adjacent)
            self.numVisits[curNode][0]-=1
        self.walkLength+=walkLength
        graphFile.close()
    
    def flushResults(self,fileName:str, topNodesLimit)->None:
        with open(fileName,'w',encoding='utf-8') as f:
            
            heapq.heapify(self.numVisits)
            visits=[]
            f.write("Random Walk Results:\n\n")
            f.write("Length of Random Walk: {}\n".format(self.walkLength))
            f.write("Top {} Pages on Wikipedia\n".format(topNodesLimit))
            for i in range(topNodesLimit):
                totalVisits ,nextBest = heapq.heappop(self.numVisits)
                f.write("{} with {} visits\n".format(self.nodeList[nextBest],-1*totalVisits))
            