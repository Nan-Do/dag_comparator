from collections import namedtuple

# This data structure represent a directed graph with a root, the graph must be
# represented using adjacency lists (using a python dictionary)
DirectedAcyclicGraph = namedtuple('DirectedAcyclicGraph', ['root',
                                                           'links'])

# This data structure represents a  subgraph for a dag  as there will only be
# one representation of the dag in memory the subgraph is reprented by its
# nodes and the root
DirectedAcyclicSubgraph = namedtuple('DirectedAcyclicSubgraph', ['root',
                                                                 'nodes'])

DirectedAcyclicSubgraphWithVariables = namedtuple('DirectedAcyclicSubgraphWithVariables',
                                                  ['graph',
                                                   'subgraph',
                                                   'variables'])
