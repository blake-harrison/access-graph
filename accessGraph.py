#!/usr/bin/env python3

__author__ = "Blake Harrison"
__copyright__ = "Copyright 2021"
__credits__ = [""]
__license__ = "GPLv3"
__version__ = "0.4.0"
__maintainer__ = ""
__email__ = "bharriso@highpoint.edu"
__status__ = "Development"
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
INF = 999999

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
def loadDijkstra(G,R,I,N):
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
    #   need to implement a fix for directed    
    for x in range(len(E)):
        start = E[x][1]
        stop = E[x][0]
        dist = E[x][2]
        graph[N.index(start)][N.index(stop)] = float(dist)
    return graph
        
def pathGraph(graph):
    path = copy.deepcopy(graph)
    for x in range(len(path)):
        for y in range(len(path)):
            for z in range(len(path)):
                if(y==z):
                    continue
                else: 
                    nextEdge = np.nansum(path[y][x]+path[x][z])
                    if(not nextEdge):
                        nextEdge = INF
                    hold = np.nanmin([path[y][z],nextEdge])
                    if(hold!=INF and hold!=np.nan):
                        path[y][z]=hold
    return path           

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
    loadDijkstra(G,R,I,N)
    graph=prepGraph(N,E) 
    path = pathGraph(graph)
    print(graph)
    print(N)
    print(path)


#executes main function
if __name__ == "__main__":
    main()