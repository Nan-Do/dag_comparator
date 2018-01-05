from collections import defaultdict


# Auxiliary function that compute all the possible successors of a
# node in a graph. Also does the  same recursively for all its
# descendants.
# TODO: Currently a recursive version, create the iterative version
def buildSuccessors(node, graph, depth, antecessors, successors):
    for antecessor in antecessors:
        if node not in successors[antecessor]:
            successors[antecessor] += ((node, depth),)

    next_antecessors = antecessors.union(node)
    for child in graph[node]:
        buildSuccessors(child, graph, depth + 1, next_antecessors, successors)


# General and  naive function to generate all the possible subgraphs of a given
# graph. Used as a reference by now
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
                              answers)
            generateSubGraphs(newNotYetConsidered.copy(),
                              soFar.union([v]),
                              graph[v],
                              answers)


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


# Old function not used anymore.
# This function uses a different model of recursion that not as
# accurate.
def _generateVariableCombinations(root,
                                  graph_nodes,
                                  graph,
                                  total_number_of_variables):
    nodes = set(graph_nodes).difference((root,))
    successors = defaultdict(tuple)
    solutions = list()

    buildSuccessors(root, graph, set(), successors)

    frontier = [(nodes, 0, ())]
    while len(frontier):
        current_nodes, number_of_variables, current_solution =\
                frontier.pop()

        # Check if the solution actually contains some elements
        # As the first solution we add is the empty set we need to
        # check it in order to not add it
        if len(current_solution):
            solutions.append(current_solution)

        # We don't want to specify more variables than the ones that
        # we specify on the function parameter
        if number_of_variables < total_number_of_variables:
            for node in current_nodes:
                # For the new solution remove  the descendants of the node
                # that we are using as a location for the variable.
                # Increase the  number of assigned variables by 1 and
                # Add the node to current temporary solutions
                frontier.append((current_nodes.difference(successors[node] +
                                                          (node,)),
                                 number_of_variables + 1,
                                 current_solution + (node,)))

    return solutions
