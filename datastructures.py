from collections import namedtuple

# This data structure represent a directed graph with a root, the graph must be
# represented using adjacency lists (using a python dictionary)
DirectedAcyclicGraph = namedtuple('DirectedAcyclicGraph', ['root', 'graph'])
