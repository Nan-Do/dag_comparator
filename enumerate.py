from collections import defaultdict

# This function creates a s expression given a graph specified as 
# dictionary of adyacency lists.
# Variables represents the positions of the graph in which we are interested
# in putting variables.
# Ex Input: 
#        a
#       / \
#       b c
#       | |
#       d f
# Output:
#    ( a ( b d ) ( c f ) )
def stringifyGraph(node, graph, variables=""):
    graph_string = ""

    # Check if the current node is marked as variable 
    if node in variables:
        graph_string = "?x" + str(variables.index(node)) + "|"
        if len(graph[node]):
            graph_string += node
        return graph_string

    if len(graph[node]):
        graph_string = "( " + node + " "
        children = []
        for child in graph[node]:
            children.append(stringifyGraph(child, graph, variables))
        graph_string += " ".join(children) + " )"
    else:
        graph_string = node

    return graph_string


# General and  naive function to generate all the possible subgraphs of a given
# graph. used as a reference by now
def generateSubGraphs(notYetConsidered, soFar, neighbors, graph, answers):
    candidates = notYetConsidered.copy()

    if len(soFar) > 0:
        candidates = candidates.intersection(neighbors)

    if len(candidates) == 0:
        answers.append(soFar)
    else:
        for v in candidates:
            newNotYetConsidered = notYetConsidered.difference([v])
            generateSubGraphs(newNotYetConsidered.copy(),
                              soFar.copy(),
                              graph[v],
                              a)
            generateSubGraphs(newNotYetConsidered.copy(),
                              soFar.union([v]),
                              graph[v],
                              a)

# Auxiliary function that compute all the possible successors of a
# node in a graph.
# TODO: Currently a recursive version, create the iterative version
def buildSuccessors(node, graph, antecessors, successors):
    for antecessor in antecessors:
        if node not in successors[antecessor]:
            successors[antecessor] += (node,)
    
    next_antecessors = antecessors.union(node)
    for child in graph[node]:
        buildSuccessors(child, graph, next_antecessors, successors)


# This function generates all the possible subgraphs given a directed
# acyclic graph and its root node.
# For each node of the graph there are three cases to generate the
# all the possible subgraphs.
# We can generates a subgraph:
#    - Using the current node
#    - Using the whole subgraph reachable from the current node
#      (For that we call the auxiliary function BuildSuccessors)
#    - Adding the current node as a leaf to the previous computed subgraphs
def generateSubGraphsDagWithRoot(root, graph):
    solutions = set()
    successors = defaultdict(tuple)
    
    buildSuccessors(root, graph, set(), successors)

    frontier = [(root, tuple())]
    while len(frontier):
        node, antecessors = frontier.pop()
        next_antecessors = antecessors + (node,)

        # Append the current node as a subgraph
        solutions.add((node,))
        # Append the whole subgraph starting from the current node
        # If we are in a leaf we shouldn't add the node as is the 
        # same as the previous case
        if len(graph[node]):
            solutions.add(tuple(successors[node]) + (node,))
            solutions.add(tuple(graph[node]) + (node,))
        # Append the graph including the antecessors until the current node
        # If antecessors is empty we are in the root and that would append
        # the root node twice
        if len(antecessors):
            solutions.add(next_antecessors)

        if len(graph[node]) and len(antecessors):
            solutions.add(tuple(next_antecessors + successors[node]))
            

        for child in graph[node]:
            frontier.append((child, next_antecessors))

    return solutions

graph = {
    "a": tuple("bc"),
    "b": tuple("d"),
    "c": tuple("f"),
    "d": tuple(""),
    "f": tuple(""),
    # "c": tuple("e"),
    # "d": tuple("h"),
    # "e": tuple(""),
    # "f": tuple(""),
    # "h": tuple("")
}

root = "a"
print stringifyGraph(root, graph, "a")
#successors = defaultdict(tuple)
#BuildSuccessors(root, graph, set(), successors)
#print successors
print map(sorted, generateSubGraphsDagWithRoot(root, graph))

