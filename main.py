from lib.createWikiGraph import WikiGraphCreator

wikiCreate = WikiGraphCreator(dumpFileLocation='./DumpFiles/enwiki-latest-pages-articles.xml.bz2',
                             graphFileLocation= './WikiGraph/graph.txt')
wikiCreate.createGraph()
wikiCreate.printStatistics()