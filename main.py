from lib.createWikiGraph import WikiGraphCreator
from lib.randomWalk import RandomWalk

wikiCreate = WikiGraphCreator(dumpFileLocation='./DumpFiles/enwiki-latest-pages-articles.xml.bz2',
                             graphFileLocation= './WikiGraph/graph.txt')    # Create a WikiGraphCreator object
# Uncomment the following line to create the graph. Ignore if graph.txt already exists
'''
wikiCreate.createGraph()        #Create graph from the bz2 file and save it to graphFileLocation
wikiCreate.completed=True       #Mark it as completed
wikiCreate.createHelperFile()   #Creates graph_helper.txt
wikiCreate.printStatistics()    #Prints statistics of the graph
'''

randomWalker = RandomWalk(wikiCreate)   #Initialize the random walker
randomWalker.loadGraph()                #Load the nodes and the offsets of adjacency list
randomWalker.randomWalk(startNode='AccessibleComputing',walkLength= 100000000)   #Start the random walk with the given start node and walk length
randomWalker.flushResults(fileName= 'Results/randomWalkResults.txt',topNodesLimit= 100) #Flush the results to a file
randomWalker.topCategories(fileName='Results/topCategories.txt',resultsFileName='Results/randomWalkResults.txt',topCategoriesLimit= 100) #Print the top categories