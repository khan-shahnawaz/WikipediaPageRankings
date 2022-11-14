import bz2
filename="./DumpFiles/enwiki-latest-pages-articles1.xml-p1p41242.bz2"
bzFile = bz2.BZ2File(filename)
c=0
for nextline in bzFile:
    pass