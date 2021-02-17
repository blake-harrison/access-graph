#!/usr/bin/env python3

__author__ = "Blake Harrison"
__copyright__ = "Copyright 2021"
__credits__ = [""]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = ""
__email__ = "bharriso@highpoint.edu"
__status__ = "Development"
#This program was built using python v3.9.1. It has not been tested with other versions.

import sys
import os.path
from os import path

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
    
    printLists(G,R,I,E)
    #print("\n\n\n")
    
    #splits each item in each list on spaces
    #i.e. ["R001 RA One"] becomes ["R001","RA","One"] 
    for x in range(len(G)):
        G[x] = G[x].split()
    for x in range(len(R)):
        R[x] = R[x].split()
    for x in range(len(I)):
        I[x] = I[x].split()
    for x in range(len(E)):
        E[x] = E[x].split()
    
    printLists(G,R,I,E)
        

#executes main function
if __name__ == "__main__":
    main()