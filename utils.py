from itertools import imap, ifilter
from collections import Counter
from datastructures import DirectedAcyclicGraph

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


def t_cost_default(s1, s2):
    """
    Auxiliary cost function to use as a example to compute the difference
    between two graphs.
    """
    max_len = len(s1)
    max_dist = ord('z') - ord('a')

    if len(s2) > len(s1):
        max_len = len(s2)

    s = abs(len(s1) - len(s2)) * max_dist
    s += sum(map(lambda x: abs(ord(x[0].lower()) -
                               ord(x[1].lower())),
                 zip(sorted(s1), sorted(s2))))

    return 1.0 - (s / float(max_len * max_dist))


def t_cost_default_distance_graphs_no_vars(g1, root_g1, g2, root_g2):
    """
    Compute the edit distance between two graphs without variables.

    g1 -> A graph as specified on the datastructures module.
    root_g1 -> The root node of the graph 1.
    g2 -> A graph as specified on the datastructures module.
    root_g2 -> The root node of the graph 2.

    g1 and g2 might be bigger graphs than the one specified by their roots.
    This is done for efficiency reasons, before computing the edit distance
    we need to compute the graphs obtained from the roots.
    """
    def reachable(g, root):
        """
        Auxiliary function to compute the reachable graphs from the roots
        """
        reachable = set()
        frontier = [root]
        while frontier:
            r = frontier.pop()
            reachable.add(r)
            frontier.extend(g.links[r])
        return reachable

    g1 = reachable(g1, root_g1)
    g2 = reachable(g2, root_g2)

    return t_cost_default(g1, g2)


def t_cost_default_distance_graphs_with_vars(m1, m2):
    """
    Compute the edit distance between two graphs with variables.

    m1 -> A mapping, that is a subgraph with a set of variables
    m2 -> A mapping, that is a subgraph with a set of variables

    The subgraphs also include the descendants of the nodes in which
    we include the variables so before we compute the edit distance
    we have to remove them from the computation
    """
    def reachable(g):
        """
        Auxiliary function to compute the reachable nodes from the
        variables.
        """
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

    return t_cost_default(set(m1.subgraph.nodes).difference(s1),
                          set(m2.subgraph.nodes).difference(s2))


def t_cost_edges_distance(g1, g1_nodes, g2, g2_nodes):
    def get_leafs(g, nodes):
        return set(map(lambda x: x[1],
                       ifilter(lambda x: x[0] in nodes and x[1] in nodes,
                               g.link_labels['I'])))

    def get_type_links(g, nodes):
        results = list()
        for node in nodes:
            links = imap(lambda x: (node, x),
                         g.links[node])
            for l in links:
                for k in g.link_labels:
                    if k == "I": continue
                    if l in g.link_labels[k]:
                        results.append(k)
                        break
        return Counter(results)

    g1_leafs = get_leafs(g1, g1_nodes)
    g2_leafs = get_leafs(g2, g2_nodes)

    l1 = get_type_links(g1, g1_nodes)
    l2 = get_type_links(g2, g2_nodes)

    matches = len(g1_leafs.intersection(g2_leafs))
    matches += sum(map(lambda x: min(l1[x], l2[x]), l1))

    return matches


def t_cost_edges_distance_graphs_no_vars(g1, root_g1, g2, root_g2):
    def reachable(g, root):
        """
        Auxiliary function to compute the reachable graphs from the roots
        """
        reachable = set()
        frontier = [root]
        while frontier:
            r = frontier.pop()
            reachable.add(r)
            frontier.extend(g.links[r])
        return reachable

    g1_nodes = reachable(g1, root_g1)
    g2_nodes = reachable(g2, root_g2)

    return t_cost_edges_distance(g1, g1_nodes, g2, g2_nodes)


def t_cost_edges_distance_graphs_with_vars(m1, m2, apply_correction=True):
    def reachable(g):
        """
        Auxiliary function to compute the reachable nodes from the
        variables.
        """
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
    
    # Adding small correction to favor solutions with more variables
    correction = 0
    if apply_correction:
        correction = 0.00000001 * (len(m1.variables) + len(m2.variables))

    return t_cost_edges_distance(m1.graph, set(m1.subgraph.nodes).difference(s1),
                                 m2.graph, set(m2.subgraph.nodes).difference(s2))\
            + correction


def t_cost_edit_distance(s1, s2):
    """
    Compute the edit distance between two set of nodes (each node is a
    character)

    The edition distance is computed as follows:
        Compute how many nodes do we have to substitute on the first graph.
        Compute how many nodes do we have to substitute on the second graph.

    Each change is weighted by its operation cost (1 by default).
    """
    g1_g2 = len(s1.difference(s2))
    g2_g1 = len(s2.difference(s1))

    return -(g1_g2 * SUBSTITUTION_COST +
             g2_g1 * SUBSTITUTION_COST)


def t_cost_edit_distance_graphs_no_vars(g1, root_g1, g2, root_g2):
    """
    Compute the edit distance between two graphs without variables.

    g1 -> A graph as specified on the datastructures module.
    root_g1 -> The root node of the graph 1.
    g2 -> A graph as specified on the datastructures module.
    root_g2 -> The root node of the graph 2.

    g1 and g2 might be bigger graphs than the one specified by their roots.
    This is done for efficiency reasons, before computing the edit distance
    we need to compute the graphs obtained from the roots.
    """
    def reachable(g, root):
        """
        Auxiliary function to compute the reachable graphs from the roots
        """
        reachable = set()
        frontier = [root]
        while frontier:
            r = frontier.pop()
            reachable.add(r)
            frontier.extend(g.links[r])
        return reachable

    g1 = reachable(g1, root_g1)
    g2 = reachable(g2, root_g2)

    return t_cost_edit_distance(g1, g2)


def t_cost_edit_distance_graphs_with_vars(m1, m2):
    """
    Compute the edit distance between two graphs with variables.

    m1 -> A mapping, that is a subgraph with a set of variables
    m2 -> A mapping, that is a subgraph with a set of variables

    The subgraphs also include the descendants of the nodes in which
    we include the variables so before we compute the edit distance
    we have to remove them from the computation
    """
    def reachable(g):
        """
        Auxiliary function to compute the reachable nodes from the
        variables.
        """
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

    return t_cost_edit_distance(set(m1.subgraph.nodes).difference(s1),
                                set(m2.subgraph.nodes).difference(s2))

if __name__ == '__main__':
    print t_cost_default(['A', 'B', 'C'], ['a', 'l'])

    links = {
             'x': ['y', 'z', 'W'],
             'y': ['B'],
             'z': ['F'],
             'W': [],
             'B': [],
             'F': [],
             }
    link_labels = {
                   'A0': set([('x', 'y')]),
                   'A1': set([('x', 'z')]),
                   'I': set([('x', 'W'), ('y', 'B'), ('z', 'F')])
                  }
    dag1 = DirectedAcyclicGraph('x', links, link_labels)
    links = {
             'a': ['b', 'c', 'W'],
             'b': ['B'],
             'c': ['b', 'G'],
             'W': [],
             'B': [],
             'G': [],
             }
    link_labels = {
                   'A0': set([('a', 'b'), ('c', 'b')]),
                   'A1': set([('a', 'c')]),
                   'I': set([('a', 'W'), ('b', 'B'), ('c', 'G')])
                  }
    dag2 = DirectedAcyclicGraph('a', links, link_labels)
    print t_cost_edges_distance_graphs_no_vars(dag1, 'x', dag2, 'a')
