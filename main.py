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