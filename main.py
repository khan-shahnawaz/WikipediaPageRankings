from lib.createWikiGraph import WikiGraphCreator
from lib.randomWalk import RandomWalk

wikiCreate = WikiGraphCreator(dumpFileLocation='./DumpFiles/enwiki-latest-pages-articles.xml.bz2',
                             graphFileLocation= './WikiGraph/graph.txt')

'''
wikiCreate.createGraph()
wikiCreate.completed=True
wikiCreate.createHelperFile()
wikiCreate.printStatistics()
'''

randomWalker = RandomWalk(wikiCreate)
randomWalker.loadGraph()
randomWalker.randomWalk(startNode='AccessibleComputing',walkLength= 1000000)
randomWalker.flushResults(fileName= 'Results/randomWalkResults.txt',topNodesLimit= 100)