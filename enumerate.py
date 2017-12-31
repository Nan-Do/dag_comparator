from collections import defaultdict
from itertools import combinations


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
                              answers)
            generateSubGraphs(newNotYetConsidered.copy(),
                              soFar.union([v]),
                              graph[v],
                              answers)


# Auxiliary function that compute all the possible successors of a
# node in a graph. Also does the  same recursively for all its
# descendants.
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


# This function generates all the source subgraphs required to put variables
# for DAGS. As input it takes a graph defined as a dictionary of adyacency
# lists and a root node. As an output it generates tuples of nodes, this
# tuples of nodes represent the the source subgraphs, the edges are the same
# as in the original graph so we don't need to store them. The set
# of source subgraphs is the minimum set of subgraphs we require in order to
# generate all the subgraphs with variables. This means that is a subgraphs
# is subsumed into another one, for example [a, b, d] and [a, b], and we
# produce both, at the moment of generating the subgraphs with variables we
# will have duplicates. The source graphs for DAGS are formed by the complete
# graph originated by the root node and the subgraphs formed by its children
# without counting the leafs. It means adding the whole graph depending of the
# root and processing its children in the same way.
# Ex:
#        a
#       / \
#       b c
#       | |
#       d e
# Returns:
#    [a, b, c, d, e]
#    [b, d]
#    [c, e]
#    [d]
#    [e]
# TODO: Add a paramater to specify a maximum depth
def generateSourceSubgraphs(root, graph):
    # We need a set as in a DAG one node can be reached by more than one path
    # and therefore there could be duplicates, using a set avoid that.
    solutions = set()
    successors = defaultdict(tuple)

    buildSuccessors(root, graph, set(), successors)

    frontier = [root]
    while len(frontier):
        node = frontier.pop()
        solutions.add(((node,) + successors[node], node))

        for child in graph[node]:
            frontier.append(child)

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


# This functions computes all the possible paths of the graph starting from
# the root using only the nodes in available nodes and returns a set with the
# reachable nodes.
# Auxiliary function used to compute all the valid positions
# in which we can put a variable.
# Ex:
#    ---a
#   |  / \
#   |  b-c
#   |  | |
#    --d e
# Available nodes: "cde"
# Output: set(['d', 'e', 'c'])
def getSelectableNodes(available_nodes, root, graph):
    reachable = set()

    frontier = list(graph[root])
    while frontier:
        node = frontier.pop()

        if node not in available_nodes:
            continue

        reachable.add(node)
        frontier.extend(graph[node])

    return reachable


# This function computes all the valid variable positions for a given graph.
# As input it takes the root node of the graph. The DAG graph and the total
# number of variables to set. As an output it returns a list of tuples, each
# tuple is a sequence of nodes, each one representing a valid position for a
# variable.
# initial_nodes is an optional parameter that represent the initial set of
# nodes that we will consider.  This allows us to consider subgraphs using
# only a set of nodes to represent it, in that case the graph must be the
# complete graph.
def generateVariableCombinations(root,
                                 graph,
                                 total_number_of_variables,
                                 initial_nodes=None):
    solutions = set()

    # Errors
    # Empty graph
    if len(graph) == 0:
        raise ValueError("Provided graph is empty")
    # Incorrect number of variables
    if total_number_of_variables <= 0:
        raise ValueError("Incorrect number of variables to assign")
    # Root not belonging to the graph
    if root not in graph:
        raise ValueError("The root does not belong to the graph")

    if initial_nodes is None:
        initial_nodes = set(graph.iterkeys())
    else:
        initial_nodes = set(initial_nodes)

    # The frontier is a tuple of 3 elements as follows:
    #  A set of nodes representing valid positions for the variables.
    #  A node that represents the father of the last processed node.
    #  A tuple representing where the variables have been set for the
    #  current configuration.
    frontier = [(initial_nodes.difference(root), root, tuple())]
    while frontier:
        selectable, father, variables = frontier.pop()

        if len(variables) < total_number_of_variables:
            for node in selectable:
                # Get the nodes in which we can put a variable
                new_selectable = getSelectableNodes(selectable.difference(node),
                                                    root,
                                                    graph)
                solution = variables + (node,)
                # To store all the possible permutations and not just a
                # combination change solutions to a list and  do not sort the
                # tuple
                solutions.add(tuple(sorted(solution)))

                # If we don't have any selectable node or the current node is
                # not a direct children of the previous father do not process
                # it. If we don't stop the recursion by controlling the father
                # we get incorrect solutions.
                if not len(new_selectable) or node not in graph[father]:
                    continue

                frontier.append((new_selectable,
                                 father,
                                 solution))

    return solutions


def generateVariableMappings(root, graph):
    source_subgraphs = generateSourceSubgraphs(root, graph)

    for (source_subgraph, source_root) in source_subgraphs:
        for combination in combinations(source_subgraph, 1):
            if combination == (source_root,):
                continue

            print stringifyGraph(source_root, graph, combination)


if __name__ == '__main__':
    root = "a"
    graph = {
        "a": tuple("bcd"),
        "b": tuple("cd"),
        "c": tuple("e"),
        "d": tuple(""),
        "e": tuple(""),
        # "c": tuple("e"),
        # "d": tuple("h"),
        # "e": tuple(""),
        # "f": tuple(""),
        # "h": tuple("")
    }

    # import pudb; pudb.set_trace()
    # print getSelectableNodes("ced", root, graph)
    print generateVariableCombinations(root, graph, 3)
    # print generateSourceSubgraphs(root, graph)
    # generateVariableMappings(root, graph)
    # print stringifyGraph(root, graph, "a")
    # successors = defaultdict(tuple)
    # BuildSuccessors(root, graph, set(), successors)
    # print successors
    # print map(sorted, generateSubGraphsDagWithRoot(root, graph))
