def stringifyGraph(dag, node, variables=[], available_nodes=[]):
    """
    This function creates a s expression given a graph specified as
    dictionary of adyacency lists.
    Variables represents the positions of the graph in which we are
    interested in putting variables.
    Ex Input:
           a
          / \
          b c
          | |
          d f
    Output:
       ( a ( b d ) ( c f ) )
    """

    graph_string = ""

    # Check if the current node is marked as variable
    if node in variables:
        graph_string = "?x" + str(variables.index(node)) + "|"
        if len(dag.graph[node]):
            graph_string += node
        return graph_string

    if len(dag.graph[node]):
        graph_string = "( " + node + " "
        children = []
        for child in dag.graph[node]:
            if available_nodes and child not in available_nodes:
                continue
            children.append(stringifyGraph(dag,
                                           child,
                                           variables,
                                           available_nodes))
        if len(children):
            graph_string += " ".join(children) + ' )'
        else:
            graph_string += ")"
    else:
        graph_string = node

    return graph_string
