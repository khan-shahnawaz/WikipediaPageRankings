import random
from .createWikiGraph import WikiGraphCreator
import heapq
from collections import defaultdict


''' Class that performs random walk on the wikigraph'''
class RandomWalk():
    def __init__(self, graph:WikiGraphCreator) -> None: #Constructor for the class
        self.helperFileName = graph.helperFileName      #Name of the helper file
        self.graphFileName = graph.graphFileName        #Name of the graph file
        self.offsetMap = {}                             #Map of node index to the offset of the adjacency list
        self.nodeList={}                                #Dictionary to store the nodename to index of node
        self.numNodes=0                                 #Number of nodes in the graph
        self.numVisits=[]                     #Array to store the number of visits to each node
        self.nodeIndex={}                               #Dictionary to store the index of node to nodename
        self.walkLength=0                               #Length of the random walk
        
    def loadGraph(self) -> None:
        ''' Loads the graph from file to the main memory'''
        with open(self.helperFileName, 'r', encoding='utf-8') as f:     #Open the helper file
            curLine = f.readline()                                      #Read the first line
            while curLine:                                              #While the line is not empty
                nodeName = curLine.strip()                              #Get the node name 
                self.nodeList[self.numNodes]= nodeName                  #Add the node name to the node list
                self.nodeIndex[nodeName]=self.numNodes                  #Add the node index to the node index list
                
                curLine = f.readline()                                  #Read the next line
                categoryOffset, outlinkOffset = curLine.strip().split(' ')      #Get the category offset and outlink offset
                self.offsetMap[self.numNodes] = (int(categoryOffset), int(outlinkOffset))   #Add the offset to the offset map
                self.numNodes+=1                                    #Increment the number of nodes
                curLine = f.readline()                            #Read the next line
        self.numVisits=[[0,i] for i in range(self.numNodes)]      #Initialize the number of visits array
    def randomWalk(self, startNode: int, walkLength: int) -> None:
        ''' Function to perform random walk on the graph'''
        curNode = self.nodeIndex[startNode]    #Get the index of the start node
        self.numVisits[curNode][0]-=1           #Increment the number of visits to the start node(We store negative of visits to use it later in the heap)
        graphFile = open(self.graphFileName, 'r', encoding='utf-8')   #Open the graph file
        for i in range(walkLength):             #For the given walk length
            if i%1000==0:                          #Print the progress
                print("Completed WalkLength of {}".format(i))       #Print the progress
            adjacent = []                #List to store the adjacent nodes      
            categoryOffset, outlinkOffset = self.offsetMap[curNode]     #Get the category offset and outlink offset
            graphFile.seek(outlinkOffset)                    #Seek to the outlink offset
            numNeighbors = int(graphFile.readline().strip())    #Get the number of neighbors
            for j in range(numNeighbors):                #For each neighbor
                neighbor = graphFile.readline().strip()     #Get the neighbor
                if neighbor not in self.nodeIndex:      #If the neighbor is not in the node index
                    continue                            #Skip it
                adjacent.append(self.nodeIndex[neighbor])   #Add the neighbor to the adjacent list
            teleport= random.randint(1,5)           #Get a random number between 1 and 5
            if len(adjacent) == 0 or teleport==1:       #If there are no neighbors or the random number is 1 then teleport
                curNode = random.randint(0, self.numNodes - 1)  #Get a random node
            else:                                    #Else
                curNode=random.choice(adjacent)    #Choose a random neighbor
            self.numVisits[curNode][0]-=1        #Increment the number of visits to the current node
        self.walkLength+=walkLength          #Increment the walk length
        graphFile.close()             #Close the graph file
    
    def flushResults(self,fileName:str, topNodesLimit)->None:
        ''' FLushes the results to a file'''
        with open(fileName,'w',encoding='utf-8') as f:  #Open the file
            
            heapq.heapify(self.numVisits)       #Create a heap from the number of visits
            f.write("Random Walk Results:\n\n")    #Write the header
            f.write("Length of Random Walk: {}\n".format(self.walkLength))  #Write the length of the random walk
            f.write("Top {} Pages on Wikipedia\n".format(topNodesLimit))    #Write the top nodes limit
            for i in range(topNodesLimit):                          #For the top nodes limit
                totalVisits ,nextBest = heapq.heappop(self.numVisits)   #Get the next best node
                f.write("{} with {} visits\n".format(self.nodeList[nextBest],-1*totalVisits))   #Write the node name and the number of visits
        
    def topCategories(self, fileName:str, resultsFileName:str, topCategoriesLimit:int)->None:
        ''' Function to get the top categories'''
        with open(fileName,'w',encoding='utf-8') as f:  #Open the file
            f.write("Top {} Categories on Wikipedia\n".format(topCategoriesLimit))    #Write the top categories limit
            resultsFile =open(resultsFileName,'r',encoding='utf-8')   #Open the results file
            resultsFile.readlines(4)  #Skip the first four lines
            curLine = resultsFile.readline()    #Read the next line
            nodes = []      #List to store the nodes
            graphFile = open(self.graphFileName, 'r', encoding='utf-8')   #Open the graph file
            visits = []      #List to store the number of visits
            while curLine:    #While the line is not empty
                lineBreak = curLine.split()  #Split the line
                lineBreak.pop()
                visits.append(int(lineBreak.pop()))   #Get the number of visits
                nodes.append(' '.join(lineBreak))     #Get the node name
                curLine = resultsFile.readline()    #Read the next line
            categories=defaultdict(int)   #Dictionary to store the category name to the number of visits
            for i in range(len(nodes)):  #For each node
                curNode = nodes[i]      #Get the node name
                categoryOffset, outlinkOffset = self.offsetMap[self.nodeIndex[curNode]]  #Get the category offset and outlink offset
                graphFile.seek(categoryOffset)   #Seek to the category offset
                for j in range(int(graphFile.readline().strip())):  #For each category
                    category= graphFile.readline().strip()   #Get the category
                    categories[category]+=visits[i]   #Increment the number of visits to the category
            for category, visits in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:topCategoriesLimit]:  #For the top categories limit
                f.write("{}\n".format(category))   #Write the category name and the number of visits
                