def GenerateSubGraphs(notYetConsidered, soFar, neighbors, graph, answers):
    candidates = notYetConsidered.copy()

    if len(soFar) > 0:
        candidates = candidates.intersection(neighbors)

    if len(candidates) == 0:
        answers.append(soFar)
    else:
        for v in candidates:
            newNotYetConsidered = notYetConsidered.difference([v])
            GenerateSubGraphs(newNotYetConsidered.copy(),
                              soFar.copy(),
                              graph[v],
                              a)
            GenerateSubGraphs(newNotYetConsidered.copy(),
                              soFar.union([v]),
                              graph[v],
                              a)

# Auxiliary function that compute all the possible successors of a
# node in a graph.
# TODO: Currently a recursive version, create the iterative version
def BuildSuccessors(node, graph, antecessors, successors):
    successors[node] = tuple()
    for antecessor in antecessors:
        if antecessor not in successors[node]:
            successors[antecessor] += (node,)
    
    next_antecessors = antecessors.union(node)
    for child in graph[node]:
        BuildSuccessors(child, graph, next_antecessors, successors)


# This function generates all the possible subgraphs given a directed
# acyclic graph and its root node.
# For each node of the graph there are three cases to generate the
# all the possible subgraphs.
# We can generates a subgraph:
#    - Using the current node
#    - Using the whole subgraph reachable from the current node
#      (For that we call the auxiliary function BuildSuccessors)
#    - Adding the current node as a leaf to the previous computed subgraphs
def GenerateSubGraphsDagWithRoot(root, graph):
    solutions = set()
    successors = dict()
    
    BuildSuccessors(root, graph, set(), successors)

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
        # Append the graph including the antecessors until the current node
        # If antecessors is empty we are in the root and that would append
        # the root node twice
        if len(antecessors):
            solutions.add(next_antecessors)
            

        for child in graph[node]:
            frontier.append((child, next_antecessors))

    return solutions

graph = {
    "a": set("bcd"),
    "b": set("d"),
    "c": set("e"),
    "d": set(""),
    "e": set("")
}

root = "a"
successors = dict()
#BuildSuccessors(root, graph, set(), successors)
#print successors
print GenerateSubGraphsDagWithRoot(root, graph)

