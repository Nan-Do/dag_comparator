# This is meant to be a global variable that indicates that the rest
# of the app should show the debugging data
DEBUG_MODE = False

SUBSTITUTION_COST = 1
DELETION_COST = 1


def stringifyGraph(dag, node, variables=[], available_nodes=[]):
    """
    This function creates a s expression given a graph specified as
    dictionary of adyacency lists.
    Variables represent the positions of the graph in which we are
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


def t_cost_function_distance(s1, s2):
    common_letters = 0

    for l in s2:
        if l in s1:
            common_letters += 1

    l1 = len(s1) - common_letters
    l2 = len(s2) - common_letters

    return -(min(l1, l2) * SUBSTITUTION_COST + abs(l1 - l2) * DELETION_COST)


def t_cost_function_distance_graphs(m1, m2):
    def reachable(g):
        reachable = list()
        for var in g.variables:
            frontier = [var]
            while frontier:
                r = frontier.pop()
                if r not in g.subgraph.nodes:
                    continue
                reachable.append(r)
                frontier.extend(g.graph.links[r])

        return reachable

    s1 = reachable(m1)
    s2 = reachable(m2)

    return t_cost_function_distance(set(m1.subgraph.nodes).difference(s1),
                                    set(m2.subgraph.nodes).difference(s2))

if __name__ == '__main__':
    print t_cost_function(['A', 'B', 'C'], ['a', 'l'])
