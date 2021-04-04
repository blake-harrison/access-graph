#!/usr/bin/env python3

__author__ = "Blake Harrison"
__copyright__ = "Copyright 2021"
__credits__ = [""]
__license__ = "GPLv3"
__version__ = "1.2.0"
__maintainer__ = ""
__email__ = "bharriso@highpoint.edu"
__status__ = "Release"
#This program was built using python v3.9.1. It has not been tested with other versions.

import sys
import os.path
import os
import copy

#note - numpy is used for array handling for the graph
#if you do not have this package installed, run:
#pip install numpy
#from a terminal
import numpy as np

#defines infinity as a global constant
#approximated at 9,999,999 because we assume no single 
#   path length will come close to this
#this can be adjusted to account for larger size values
INF = 9999999

#reads in the input file
#takes 5 parameters:
#   inFile - the name of the input file
#   G - list to hold the grocery stores (nodes)
#   R - list to hold the residential areas (nodes)
#   I - list to hold the intersections (nodes)
#   E - list to hold the roads (edges)
def readFile(inFile, G, R, I, E):
    #first checks if the file exists in the current folder
    if (os.path.exists(inFile)):
        #opens the input file
        with (open(inFile,'r')) as file:
            isNodes = True
            ln = 0
            for line in file:
                ln += 1
                
                #designates the start of the edges
                if line[0] == '<' and line[1] == 'E':
                    isNodes = False
                    
                #if nodes are being read in (default case)
                if isNodes:
                    #ignores the <NODES> designator
                    if line[0] == '<' and line[1] == 'N':
                        continue
                    #case: grocery store
                    elif line[0] == 'G':
                        G.append(line.replace("\n",""))
                    #case: residential area
                    elif line[0] == 'R':
                        R.append(line.replace("\n",""))
                    #case: intersection
                    elif line[0] == 'I':
                        I.append(line.replace("\n",""))
                    #case: invalid input
                    else: sys.exit("Error: Invalid Input Detected on Line " + str(ln) + " in file '" + inFile + "'\n")
                
                #if edges are being read in
                else:
                    #ignores the <EDGES> designator
                    if line[0] == '<' and line[1] == 'E':
                        continue
                    #reads in a node
                    else: 
                        E.append(line.replace("\n",""))     
    else:
        os.system('cls' if os.name == 'nt' else 'clear') 
        sys.exit("Error: Invalid Input File Name: '" + inFile + "' could not be found.")           

#prints the lists - used primarily for debugging purposes
#takes in 4 lists:
#   G (the grocery stores) 
#   R (residential areas) 
#   I (intersections) (our artificial nodes for connectivity purposes)
#   E (roads (edges))           
def printLists(G,R,I,E):
    print("\nG = ", G)
    print("R = ", R)
    print("I = ", I)
    print("E = ", E)
    print("\n")

#loads all of the nodes into one list:
#takes in 4 lists:
#   G (the grocery stores) 
#   R (residential areas) 
#   I (intersections) (our artificial nodes for connectivity purposes)
#   N (a list that will be filled all of the nodes)      
#       note: other functions require that the nodes be loaded in this order,
#       or they will not function correctly
def loadNodes(G,R,I,N):
    for x in range(len(G)):
        N.append(G[x][0])
    for x in range(len(R)):
        N.append(R[x][0])
    for x in range(len(I)):
        N.append(I[x][0])

#turns the lists of nodes and edges into one graph
#takes in 2 lists:
#   N (all the nodes)
#   E (all the edges)
#
#returns a two-dimensional list acting as the graph
def prepGraph(N,E):
    
    #sets up an empty array of correct dimensions
    #fills the array with the value nan as a placeholder
    graph=np.empty((int(len(N)),int(len(N)))) * np.nan
    
    #loops through the edges, initializing the graph
    for x in range(len(E)):
        start = E[x][0]
        stop = E[x][1]
        dist = E[x][2]
        graph[N.index(start)][N.index(stop)] = float(dist)
    #IMPORTANT: this is set up to treat every edge as undirected
    #   need to implement a fix to allow for directed nodes  
    for x in range(len(E)):
        start = E[x][1]
        stop = E[x][0]
        dist = E[x][2]
        graph[N.index(start)][N.index(stop)] = float(dist)
    return graph

#Computes the floyd-warshall algorithm with the given graph
#   the input graph should hold an adjacency matrix for all the nodes
#   returns path, the completed floyd-warshall matrix
#       each [x][y] holds the shortest distance from node x to node y
def pathGraph(graph):
    #creates a deep copy of graph to prevent shallow copy errors
    path = copy.deepcopy(graph)
    
    for x in range(len(path)):
        for y in range(len(path)):
            for z in range(len(path)):
                #shortest distance from node to itself will always be nan
                if(y==z):
                    continue
                else: 
                    
                    #sums the distances betwen the next two edges, treating nan as 0
                    #NOTE - this is probably going to cause errors if [y][x] is nan and 
                    #   [x][z] is not (or vice versa) - test this more
                    nextEdge = np.nansum(path[y][x]+path[x][z])
                    
                    #both of the next two edges are nan
                    if(not nextEdge):
                        nextEdge = INF
                        
                    #gets the minimum value between path[y][z] and nextEdge
                    hold = np.nanmin([path[y][z],nextEdge])
                    
                    #if hold is INF or nan, then no path exists between the two nodes
                    #otherwise, sets [y][z] to hold 
                    if(hold!=INF and hold!=np.nan):
                        path[y][z]=hold
    return path           

#finds the average distance from a node to a range of other nodes
#takes in the graph and 3 integers (graph indicies):
#   start is the index of the first element in the range
#   stop is the index of the last element in the range
#   num is the number of elements to take from the range,
#       prioritizing the nearest nodes
#   node is the point of origin
#   returns the average distance from node to a number of nodes (num)
#       from graph, in that range (start,stop)
#   If 
def avgDist(graph,start,stop,num,node):
    hold = []
    short = []
    nanCount = 0
    pathSum = 0
    
    #if num is not a valid input
    if(num > stop-start or num <= 0):
        sys.exit("Error: Improper Number of Nodes Requested. You must request a numer of nodes greater than 0 but less than or equal to the amount of G-nodes the graph has.\n Your graph has " + str(stop-start) + " G-nodes.\n You requrested " + str(num) + " G-nodes.\n")  
    
    #appends hold with the lengths of all existing paths
    for x in range(start,stop):
        if(graph[node][x]!=np.nan):
            hold.append(graph[node][x])
    
    #appends short with each length in order from shortest to longest
    #after a value has been added, it is set to our infinity approximation
    for y in range(len(hold)):
        val = np.nanmin(hold)
        if(val!=INF and val!=np.nan):
            short.append(val)
        hold[hold.index(val)]=INF
        
    #handles if the amount of added path lengths are less than the requested number
    # (this should only be true if the node does not have a path to some of the nodes
    #  in the start-stop range)
    if(len(short)<=num):
        num = len(short)
        
    #sums the num smallest lengths
    for z in range(num):
        pathSum += short[z]
    return pathSum/num

#returns an ordered list of all the nodes R ranked by average distance to G nodes
#takes in:
#   graph, a the final shortest path matrix
#   G, the number of nodes that correspond to grocery stores
#   R, the number of nodes that correspond to residential areas
#   num, the number of grocery stores to get for each residential area
#       (prioritizing the nearest grocery stores)
#   top, the number of elements to return
#   far, a boolean that returns the nodes with the farthest avg distance if true, and 
#       the least average distance if false.
#       By default, this value is set to True
def getIsol(graph,G,R,num,far = True):
    hold = []
    order = []
    
    #calculates the average distance to the grocery stores for each residential node
    for i in range(G,G+R):
        hold.append([avgDist(graph,0,G,num,i),i])
    
    #orders the nodes by the shortest avg distance to num grocery stores
    for j in range(len(hold)):
        val = hold[j][0]
        sIndex = j
        for k in range(len(hold)):
            if(val>hold[k][0] and hold[k][0]!=INF):
                val=hold[k][0]
                sIndex = k
        order.append(copy.deepcopy(hold[sIndex]))
        hold[sIndex][0] = INF
        
    #if the user wants the closest instead of farthest
    if(not far):
        close = []
        #copies the list in reverse
        #probably more efficient ways to do this, maybe fix it later
        for x in range(num):
            close.append(copy.deepcopy(order[-x]))
        return close
    #default setting
    else:
        return order

#outputs a number of results
#takes in several parameters:
#   R is the list of residential area nodes
#   order is a list containing each residential node
#       and its average distance to a set number of G-nodes
#       Order is obtained from the getIsol function
#   gNum is the number of G-nodes
#   top is the number of results to output
#       by default this is set to the length of order (printing all results)
def getTop(R, order, gNum, top = INF):
    print("Residential Area     Average Distance to Grocery Store")
    
    #default setting, prints all 
    if top == INF:
        top = len(order)
    for x in range(top):
        printStr = ""
        numStr = ""
        
        #takes the length of each string in R, ignores the R### code
        for y in range(1,len(R[order[x][1]-gNum])):
            printStr += str(R[order[x][1]-gNum][y])
            printStr += " "
        printStr = printStr.ljust(30) 
        #adds the average distance
        numStr += str("{:.4f}".format(order[x][0]/1000))
        numStr += " km"
        printStr += numStr.rjust(5)
        print(printStr)       

def main():
    run = True
    badInput = False    
    inFile = ""
    #creates lists to hold each set of nodes
    G = [] #holds grocery stores
    R = [] #holds residential areas
    I = [] #holds intersections
    E = [] #holds edges
    
    while(run):
        userIn = printMenu(badInput,inFile)
        if(userIn == '1'):
            badInput = False
            os.system('cls' if os.name == 'nt' else 'clear')
            
            #reads the input file in
            inFile = input("\nPlease Enter the Name of Your Datafile:\n\n\n\n")
            readFile(inFile,G,R,I,E)
        
            #splits each item in each list on spaces
            #i.e. ["R001 RA One"] becomes ["R001","RA","One"] 
            for x in range(0,len(G)):
                G[x] = G[x].split()
            for x in range(0,len(R)):
                R[x] = R[x].split()
            for x in range(0,len(I)):
                I[x] = I[x].split()
            for x in range(0,len(E)):
                E[x] = E[x].split()
                
            #adds a list that holds N, which contains all the nodes
            N=[]
            loadNodes(G,R,I,N)
    
            #gets the adjacency matrix
            graph=prepGraph(N,E) 
    
            #gets the Floyd-Warshall matrix from the adjacency matrix
            path = pathGraph(graph)
            
            #gets the average distance to a number of grocery stores for each node,
            #   then orders them from most avg dist to greatest
            order = []
            order = getIsol(path,len(G),len(R),len(G))
            
            print("\n\n\nFile Loaded Successfully")
            print("\n\n\n\n\n\n\n")
            input("Press Enter to Continue...")
                
        elif(userIn == '2'):
            os.system('cls' if os.name == 'nt' else 'clear')
            #prints the output
            print("\n")
            getTop(R,order,len(G))
            print("\n\n\n")
            input("Press Enter to Continue...")
            
        
        elif(userIn == '3'):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nComing Soon\n\n\n")
            input("Press Enter to Continue...")
        
        elif(userIn == '4'):
            os.system('cls' if os.name == 'nt' else 'clear')
            run = False
        
        else:
            badInput = True
    
#prints the user menu
#   badInput is a boolean triggered if the user sends bad input
#   inFile is the current input file
#   if not called with a file name, assumes there is no loaded file
def printMenu(badInput = False, inFile = ""):
    if inFile == "":
        inFile = "No File Loaded"
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""   
           _____ _____ ______  _____ _____ 
    /\   / ____/ ____|  ____|/ ____/ ____|
   /  \ | |   | |    | |__  | (___| (___  
  / /\ \| |   | |    |  __|  \___ \\___ \ 
 / ____ | |___| |____| |____ ____) ____) |
/______\_______\_____|____________|_____/ 
 / ____|  __ \    /\   |  __ \| |  | |    
| |  __| |__) |  /  \  | |__) | |__| |    
| | |_ |  _  /  / /\ \ |  ___/|  __  |    
| |__| | | \ \ / ____ \| |    | |  | |    
 \_____|_|  \_/_/    \_|_|    |_|  |_|                                          
                                                  """)
    print("""\
    WELCOME TO ACCESS GRAPH, v1.2.0
        
    Please select:
            
    1) Read New File
        
    2) Get Output
        
    3) Settings
        
    4) Quit
        
        """)
    print("\n   Current File: " + inFile + "\n\n")
    
    if(badInput):
        print("\n   Error: Invalid Input. Please Try Again\n\n")
    
    return input()


#executes main function
if __name__ == "__main__":
    main()