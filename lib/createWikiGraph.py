import bz2
import xml.etree.ElementTree as ET
import re
import time

''' Class that creates wikigraph file'''
class WikiGraphCreator():
    def __init__(self, dumpFileLocation:str, graphFileLocation:str)->None:
        ''' Constructor to Open files and initialise variables'''
        
        
        self.dumpFileName=dumpFileLocation  #Location of the dump file
        self.graphFileName=graphFileLocation    #Location of the graph file
        self.helperFileName = graphFileLocation[:-4]+"_helper.txt"  #Open helper file
        self.totalTime=0                                    #Total time taken to create the graph
        self.completed=False                                #Flag to check if graph is created
        self.totalNodes=0                        #Total number of nodes in the graph
        self.totalEdges=0               #Total number of edges in the graph
        self.totalCategories=0      #Stores sum of all categories marked for all nodes
        
    def createGraph(self)->None:
        ''' Creates wikigraph for the object '''
        self.bzFile = bz2.BZ2File(self.dumpFileName)    #Open the bz2 file
        self.graphFile = open(self.graphFileName,'w',encoding='utf-8')  #Open the graph file
        startTime=time.time()       #Record start time
        
        while True:
            nextLine=self.bzFile.readline() #Fetch next line
            if not nextLine:               #If end of file reached
                ''' Break if EOF detected '''
                break
            
            line=str(nextLine, 'utf-8').strip() #Convert to string and strip
            
            if line=="<page>":      #If page tag detected
                if self.totalNodes%1000000==0:          #Print progress
                    print("Completed {} Nodes".format(self.totalNodes))
                ''' If a new page starts'''
                categories=[]       #List to store categories of the node
                outEdges=[]         #List of links from the page
                pageLines=[]        #List of lines in the page to parse it later
                self.totalNodes+=1  #Increment total nodes
                while line!="</page>":  #Read till end of the current page
                    pageLines.append(line)  #Append the line to the list pageLines
                    line=str(self.bzFile.readline(),'utf-8').strip()    #Read next line
                    
                pageLines.append(line)  #Append the last line to the list pageLines
                pageRoot = ET.fromstring("\n".join(i for i in pageLines))   #Creates XML Trees
                for child in pageRoot:      #Iterate over all the children of the root
                    if child.tag=='title':  #If title tag detected
                        title=child.text    #Store the title
                        if '\n' in title:   #If the title does not contain newline then its a valid title
                            continue
                        self.graphFile.write(title) #Write the title to the graph file
                        self.graphFile.write('\n')  #Write a newline as per the format
                        
                    for nextchild in child:         #Iterate through the child of the current child
                        if nextchild.tag=='text':   # Detects the text section
                            if not nextchild.text:  # If the text section is empty
                                continue            #Ignore the section
                            listOfLinks=re.findall('\[\[([^\[\]]+)\]\]',nextchild.text)     #Find all the links in the text section by regex
                            for link in listOfLinks:        #Iterate through all the links
                                link=str(link.split('|')[0])    #Split the link by | and take the first part as the link
                                if '\n' in link:                #If the link contains newline then its not a valid link
                                    continue
                                if link.startswith('Category:'):     #If the link is a category   
                                    categories.append(link[9:])         #Append the category to the list of categories
                                    self.totalCategories+=1             #Increment the total number of categories
                                else:
                                    if 'Link:' not in link and 'File:' not in link and 'Wikipedia:' not in link and 'Help:' not in link:    #If the link is not a file or wikipedia tag
                                        outEdges.append(link)    #Append the link to the list of outlinks
                                        self.totalEdges+=1          #Increment the total number of edges
                
                
                self.graphFile.write(str(len(categories)))      #Write the number of categories to the graph file
                self.graphFile.write('\n')            #Write a newline as per the format
                for category in categories:          #Iterate through all the categories
                    self.graphFile.write(category)      #Write the category to the graph file
                    self.graphFile.write('\n')          #Write a newline as per the format
                self.graphFile.write(str(len(outEdges)))    #Write the number of outlinks to the graph file
                self.graphFile.write('\n')                  #Write a newline as per the format
                for outEdge in outEdges:                    #Iterate through all the outlinks
                    self.graphFile.write(outEdge)           #Write the outlink to the graph file
                    self.graphFile.write('\n')                  #Write a newline as per the format
        endTime=time.time()                             #Record end time
        self.totalTime=(endTime-startTime)              #Calculate total time taken
        self.completed=True                             #Set the flag to true 
        self.bzFile.close()                        #Close the bz2 file
        self.graphFile.close()                      #Close the graph file
        
    ''' Function to create helper file which stores the offset of each node in the graph file'''
    def createHelperFile(self)->None:           
        ''' Creates a helper file for the wikigraph '''
        if not self.completed:      #If the graph is not created
            print("Please create the graph first")  #Print error message
            return                                #Return
        helperFile=open(self.graphFileName[:-4]+"_helper.txt",'w',encoding='utf-8') #Open the helper file
        self.graphFile=open(self.graphFileName,'r',encoding='utf-8')    #Open the graph file
        curLine= self.graphFile.readline()  #Read the first line
        while curLine:                    #Iterate till the end of the file
            nodeName=curLine.strip()        #Store the node name
            
            categoryOffset=self.graphFile.tell()        #Store the offset of the categories
            numCategory=int(self.graphFile.readline().strip())  #Store the number of categories
            for i in range(numCategory):            #Iterate through all the categories
                self.graphFile.readline()           #Read the category
            outlinkOffset=self.graphFile.tell()     #Store the offset of the outlinks
            numOutLinks=int(self.graphFile.readline().strip())      #Store the number of outlinks
            for i in range(numOutLinks):            #Iterate through all the outlinks
                self.graphFile.readline()           #Read the outlink
            helperFile.write(nodeName)              #Write the node name to the helper file
            helperFile.write('\n')                  #Write a newline as per the format
            helperFile.write(str(categoryOffset)+' '+str(outlinkOffset)+'\n')   #Write the offset of the categories and outlinks to the helper file
            curLine=self.graphFile.readline()           #Read the next line
        helperFile.close()                                  #Close the helper file
        return
    
    def printStatistics(self)->None:
        ''' Prints the statistics of the graph created'''
        print("WikiGraph created from dump {} and stored in {}".format(self.dumpFileName, self.graphFileName))  #Print the name of the dump file and the graph file
        print("Total Time Taken:",self.totalTime,'seconds')   #Print the total time taken
        print("Number of Pages:", self.totalNodes)  #Print the total number of nodes
        print("Number of outLinks:", self.totalEdges)   #Print the total number of edges
        print("Total Number of Categories(with duplicates) across all pages:",self.totalCategories) #Print the total number of categories
        return  #Return