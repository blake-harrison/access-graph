#!/usr/bin/env python3

__author__ = "Blake Harrison"
__copyright__ = "Copyright 2021"
__credits__ = [""]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = "bharriso@highpoint.edu"
__status__ = "Release"
#This program was built using python v3.9.1. It has not been tested with other versions.

import sys
import os.path
from os import path
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
    if (path.exists(inFile)):
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
    else: sys.exit("Error: Invalid Input File Name: '" + inFile + "' could not be found.")           

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
    if(num > stop-start or num <= 0):
        sys.exit("Error: Improper Number of Nodes Requested. You must request a numer of nodes greater than 0 but less than or equal to the amount of G-nodes the graph has.\n Your graph has " + str(stop-start) + " G-nodes.\n You requrested " + str(num) + " G-nodes.\n")  
    for x in range(start,stop):
        if(graph[node][x]!=np.nan):
            hold.append(graph[node][x])
    for y in range(len(hold)):
        val = np.nanmin(hold)
        if(val!=INF and val!=np.nan):
            short.append(val)
        hold[hold.index(val)]=INF
    if(len(short)<=num):
        num = len(short)
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
    for i in range(G,G+R):
        hold.append([avgDist(graph,0,G,num,i),i])
    for j in range(len(hold)):
        val = hold[j][0]
        sIndex = j
        for k in range(len(hold)):
            if(val>hold[k][0] and hold[k][0]!=INF):
                val=hold[k][0]
                sIndex = k
        order.append(copy.deepcopy(hold[sIndex]))
        hold[sIndex][0] = INF
    if(not far):
        close = []
        for x in range(num):
            close.append(copy.deepcopy(order[-x]))
        return close
    else:
        return order

def getTop(R, order, gNum, top):
    print("Residential Area     Average Distance to Grocery Store")
    for x in range(top):
        printStr = ""
        numStr = ""
        for y in range(1,len(R[order[x][1]-gNum])):
            printStr += str(R[order[x][1]-gNum][y])
            printStr += " "
        printStr = printStr.ljust(30) 
        numStr += str("{:.4f}".format(order[x][0]/1000))
        numStr += " km"
        printStr += numStr.rjust(5)
        print(printStr)       

def main():
    #user specifies the input file
    inFile = input("\n\n\n\nPlease Enter the Name of Your Datafile:\n")
    print("\n\n\n")
    
    #creates lists to hold each important part
    G = [] #holds grocery stores
    R = [] #holds residential areas
    I = [] #holds intersections
    E = [] #holds edges
    
    #reads the input file in
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
    graph=prepGraph(N,E) 
    path = pathGraph(graph)
    #print(graph)
    #print("\n")
    #print(N)
    #print("\n")
    #print(path)
    
    order = []
    order = getIsol(path,len(G),len(R),len(G))
    #print(order)
    getTop(R,order,len(G),len(order))
    print("\n\n\n")

#executes main function
if __name__ == "__main__":
    main()