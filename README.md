# access-graph
This program uses a version of the Floyd-Warshall algorithm to analyze a user-defined graph.

## Purpose
This program was initially created to analyze food security within the city of High Point, North Carolina. It is intended to be open-source and modular, to allow users to apply this algorithm to other areas for access to food.


## Function
The user input will contain three different types of nodes:


- R nodes, which designate a residential area
- G nodes, which designate a grocery store (or other food retailer)
- I nodes, which serve as "intersections". Their sole purpose is to enhance the connectivity of the graph

The program will read these in (along with a list of edges) and then calculate the average distance for each R node to the nearest user-defined number (default: 3) of G nodes. 

## Preparation
You should ensure that you have met the following criteria before you run this program:

1. Python


This program was tested for compatability with Python versions 3.8.5 or later.


If you do not have python, you can install it with the following link: (https://www.python.org/downloads/)


If you have python installed, you should be able to open a command prompt and type:


`python --version`, which should tell you the current installed version of python (if any)

2. Packages


Once you have python installed, you need to install the numpy package, which this program relies on.


Open a command prompt, and run:


`pip install numpy`

3. Input File


You must format your input file in a manner similar to that of the included sample.txt file.


The order of your nodes does not matter (i.e. you can have G or I first), however, you must have the \<NODES\> and \<EDGES\> markers. 

In addition, each node line must take the format:


`R### Name of Node`


and each edge line must take the format:


`<node 1 code> <node 2 code> <distance between nodes>` 


For more information about how you can gather data for an input file, you can watch the following video: (link)

## Using the Program


To use the program, open a command prompt and navigate to the directory where you saved the accessGraph.py file.


Then, run:


`python3 accessGraph.py`


The user menu will open and prompt you for input. Enter the number corresponding to the desired option.

When reading from an input file, make sure that your input file is in the same directory as the accessGraph.py file.
If it is not there, you need to either move it or provide a relative/absolute filepath to the program.


## Example
I am running macOS and have saved the files in my 'Downloads' folder.


I can open a command prompt (Applications -> Utilities -> Terminal) and it will by default place me in my home directory.


From there, I can enter the following command:


`cd Downloads`


I can then enter the command:


`ls` 


to see the contents of my folder (looking specifically for the accessGraph.py program and my input file, sample.txt)


Then, I can do:


`python3 accessGraph.py`


And it will launch the program.


From the main menu, I can enter '1' to read a new file. When prompted, I will enter:


`sample.txt`


Then hit enter to return to the main menu once the program tells me the file has been successfully read.


From the main menu, I can then enter '2' to see my results.