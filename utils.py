# This is meant to be a global variable that indicates that the rest
# of the app should show the debugging data
DEBUG_MODE = False


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
        if len(dag.links[node]):
            graph_string += node
        return graph_string

    if len(dag.links[node]):
        graph_string = "( " + node + " "
        children = []
        for child in dag.links[node]:
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


def t_cost_function(s1, s2):
    max_len = len(s1)
    max_dist = ord('z') - ord('a')

    if len(s2) > len(s1):
        max_len = len(s2)

    s = abs(len(s1) - len(s2)) * max_dist
    s += sum(map(lambda x: abs(ord(x[0].lower()) -
                               ord(x[1].lower())),
                 zip(sorted(s1), sorted(s2))))

    return 1.0 - (s / float(max_len * max_dist))


def sort_by_num_of_variables(v):
    max_num_of_variables = 0

    for x in v:
        if len(x.variables) > max_num_of_variables:
            max_num_of_variables = len(x.variables)
    answers = tuple([[] for _ in xrange(max_num_of_variables)])

    for x in v:
        answers[len(x.variables)-1].append(x)

    return answers


if __name__ == '__main__':
    print t_cost_function(['A', 'B', 'C'], ['a', 'l'])
