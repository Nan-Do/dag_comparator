from collections import defaultdict
from copy import deepcopy
from itertools import chain
from random import choice, shuffle, normalvariate, randint
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits

import argparse
import logging
import sys

DEBUG = True


def random_id_generator(size=6, chars=ascii_letters+digits):
    """
    Generate a random id.

    size -> The size of the generated id.
    chars -> The pool of characters to choose to generate the id.

    Returns a string.
    """
    return ''.join(choice(chars) for _ in range(size))


def print_graph(graph, treelevels):
    """
    Pretty printer function for the graph.

    graph -> graph as a dictionary of lists (adjacency lists)
    treelevels -> a lists of lists representing the tree.
    """
    leafs = set([key for key in graph if not len(graph[key])])
    for node in chain.from_iterable(chain.from_iterable(treelevels[:-1])):
        if node not in leafs:
            print '  ', node, ":", graph[node]
    print "  Leafs:", leafs


def get_chunks(seq, size, step=1):
    """
    Split a sequence into chunks of different sizes specified by
    size.

    seq -> The sequence to split.
    size -> Size of the chunks
    step -> How much to move on the original list before generating
            the next chunk.

    Similar to partition in clojure, it returns a generator for the
    chunks.
    """
    for x in xrange(0, len(seq) - size + step, step):
        yield seq[x:x+size]


def graph_to_image(graph, filename):
    """
    Generate an image of a graph and store at a file.

    graph -> the graph specified as a dictionary of lists.
    filename -> the file name in which to store the image.

    The picture follows the dot format
    """
    import networkx as nx
    from networkx.drawing.nx_agraph import write_dot, graphviz_layout
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    for k in graph:
        G.add_node(k)
        G.add_nodes_from(graph[k])
        for v in graph[k]:
            G.add_edge(k, v)

    write_dot(G, filename + ".dot")
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=True, arrows=False)
    plt.savefig(filename + ".png")


def generate_pool_nodes(size, lower=True):
    """
    Generate a pool of elements that will be used as a nodes for the graph.

    size -> The size of the pool.
    lower -> Use lower or upper case letters for the pool.

    Returns a list.
    """
    if lower:
        letters = list(ascii_lowercase)
    else:
        letters = list(ascii_uppercase)

    if size <= len(letters):
        return letters
    elif size <= len(letters) + len(digits):
        return letters + list(digits)
    else:
        return range(1, size)


def generate_nodelists(nodes, num_lists, average_size, dispersion=1):
    """
    Generate lists of nodes.

    nodes -> The pool from which we extract the nodes of the graph.
    num_lists -> The total number of lists to generate.
    average_size -> The average size of the lists to generate.
    dispersion -> The dispersion of the generated lists.

    Returns a list of lists.
    Average_size and dispersion are used to characterize a normal distribution.
    This version is better to honor the condition that given an average size
    all the nodes with descecndants will have at most average size
    descecndants.
    """
    result = []
    pool = [x for x in nodes]
    shuffle(pool)

    total = 0
    for _ in xrange(num_lists):
        l = []
        x = int(normalvariate(average_size, dispersion))
        if x == 0:
            x = 1
        total += x
        for _ in xrange(x):
            if len(pool):
                l.append(pool.pop())
            else:
                break
        if len(l):
            result.append(l)
    return result


def __generate_nodelists(nodes, average_size, dispersion=1):
    """
    Generate lists of nodes.

    nodes -> The pool from which we extract the nodes of the graph.
    average_size -> The average size of the lists to generate.
    dispersion -> The dispersion of the generated lists.

    Returns a list of lists.
    Generates lists until it consumes the whole pool.
    Average_size and dispersion are used to characterize a normal distribution.
    """
    result = []
    pool = [x for x in nodes]
    shuffle(pool)

    total = 0
    while len(pool):
        l = []
        x = int(normalvariate(average_size, dispersion))
        if x == 0:
            x = 1
        total += x
        for _ in xrange(x):
            if len(pool):
                l.append(pool.pop())
        if len(l):
            result.append(l)
    return result


def generate_treelevels(root, nodelists, depth):
    """
    Generate the levels of the the tree using the nodelists.

    root -> root of the tree.
    nodelists -> A list of lists containing nodes.
    depth -> The depth of the tree

    Return a list of lists.
    """
    res = [[[root]], [nodelists[0]]]

    lists_per_level = (len(nodelists) - 1) / (depth - 2)
    if lists_per_level <= 0:
        logging.warning("The specified depth is too big")
        lists_per_level = 1

    return res + list(get_chunks(nodelists[1:],
                                 lists_per_level,
                                 lists_per_level))


def normalize_treelevels(treelevels):
    """
    Normalize the treelevels so they can be used to generate the tree without
    problems.

    treelevels -> The list of lists containing the levels of the tree.

    The normalized treelevels must fulfill the condition that at any given
    level the number of nodes of that level must be at least equal (or higher)
    than the number of blocks of the next level. With the exepction of the
    root.
    """
    root = treelevels.pop(0)

    while True:
        modified = False
        for x, y in get_chunks(treelevels, 2, 1):
            if len(list(chain.from_iterable(x))) < len(y):
                modified = True
                # Find the smallest block of y and move it
                # to the previous level
                position = 0
                min_value = float('inf')
                for pos, value in enumerate(map(len, y)):
                    if min_value < value:
                        position = pos

                x.append(y[position])
                y.pop(position)

        if not modified:
            break

    treelevels.insert(0, root)


def generate_tree(treelevels):
    """
    Generate a tree from the normalized tree levels

    treelevels -> A list of lists representing the levels of a tree.

    Returns a dictionary of lists
    """
    tree = defaultdict(list)

    # Process the root
    root = treelevels[0][0][0]
    for x in chain.from_iterable(treelevels[1]):
        tree[root].append(x)

    # Process the leaves
    for node in chain.from_iterable(treelevels[-1]):
        tree[node]

    for x, y in get_chunks(treelevels[1:], 2):
        election_nodes = (list(chain.from_iterable(x)))
        shuffle(election_nodes)

        for node in election_nodes:
            tree[node] = []
        for block in y:
            if not election_nodes:
                logging.error("The tree levels are not normalized")
                sys.exit(0)

            orig_node = election_nodes.pop()
            for dest_node in block:
                tree[orig_node].append(dest_node)

    return tree


def generate_dag(graph, num_of_links, treelevels):
    """
    Generate a DAG from a tree.

    graph -> The tree we will use to generate the DAG.
    num_of_links ->  The number of extra links to add to the tree.
    treelevels -> the tree split into a list of levels

    The function mutates the graph adding the new links
    """
    while num_of_links > 0:
        # Get the source node
        source_block = randint(0, len(treelevels) - 2)
        source_node = choice(choice(treelevels[source_block]))

        # Get the destination node
        dest_block = randint(source_block+1, len(treelevels) - 1)
        dest_node = choice(choice(treelevels[dest_block]))

        # Check that the link doestn't exist already
        if dest_node in graph[source_node]:
            continue

        graph[source_node].append(dest_node)
        num_of_links -= 1


def swap_nodes(graph, source_node, dest_node):
    for nodes_list in graph.itervalues():
        if source_node in nodes_list and dest_node in nodes_list:
            index = nodes_list.index(source_node)
            nodes_list.pop(index)
            nodes_list.insert(index, dest_node)

            index = nodes_list.index(dest_node)
            nodes_list.pop(index)
            nodes_list.insert(index, source_node)
        elif source_node in nodes_list:
            index = nodes_list.index(source_node)
            nodes_list.pop(index)
            nodes_list.insert(index, dest_node)
        elif dest_node in nodes_list:
            index = nodes_list.index(dest_node)
            nodes_list.pop(index)
            nodes_list.insert(index, source_node)

    temp = graph[source_node]
    graph[source_node] = graph[dest_node]
    graph[dest_node] = temp


def change_node(graph, node_to_be_changed, node_to_change_to):
    for nodes_list in graph.itervalues():
        if node_to_be_changed in nodes_list:
            index = nodes_list.index(node_to_be_changed)
            nodes_list.pop(index)
            nodes_list.insert(index, node_to_change_to)

    temp = graph[node_to_be_changed]
    del graph[node_to_be_changed]
    graph[node_to_change_to] = temp


if __name__ == '__main__':
    size = 25
    outdegree = 3
    depth = 3

    parser = argparse.ArgumentParser(description="Generate random acyclic directed graphs")

    parser.add_argument("--size", dest="size",
                        type=int,
                        help="Choose the size of the graph (default 25)")

    parser.add_argument("--out", dest="out",
                        type=int,
                        help="Choose the outdegree of the graph (default 3)")

    parser.add_argument("--depth", dest="depth",
                        type=int,
                        help="Choose the depth of the graph")

    parser.add_argument("--upper", dest="upper", action="store_true",
                        help="Use upper case instead lower case")

    parser.add_argument("--image", dest="image",
                        type=str,
                        help="Generate an image of the generated graph")

    parser.add_argument("--dag", dest="dag",
                        type=str,
                        help="Specify the density of the dag, if not specified it will generate a tree",
                        choices=["sparse", "medium", "dense"])

    parser.add_argument("--swap", dest="swap",
                        type=int,
                        help="Perturbation that swaps two nodes. This operation is repeated SWAP times")

    parser.add_argument("--change", dest="change",
                        type=int,
                        help="Perturbation that changes one node with a label from outside the domain. This operation is repeated CHANGE  times")

    args = parser.parse_args()

    if args.size:
        size = args.size

    if args.out:
        outdegree = args.out

    if args.depth:
        depth = args.depth

    # Create the node pools of each graph
    pool_of_nodes = generate_pool_nodes(size)

    # Select the root
    root = choice(pool_of_nodes)
    pool_of_nodes.remove(root)

    # Stablish the number of lists for each graph
    num_of_lists = (size - 1) / outdegree

    lists_of_nodes = generate_nodelists(pool_of_nodes, num_of_lists, outdegree)
    if DEBUG:
        number_of_nodes = len(list(chain.from_iterable(lists_of_nodes)))
        print "Number of nodes for the graph:", number_of_nodes, '/', size
        print

    treelevels = generate_treelevels(root, lists_of_nodes, depth)

    if DEBUG:
        print "Generated Lists:"
        for pos, x in enumerate(treelevels):
            print '  ', pos, x
        print
    normalize_treelevels(treelevels)

    if DEBUG:
        print "Normalized Lists:"
        for pos, x in enumerate(treelevels):
            print '  ', pos, x
        print

    graph = generate_tree(treelevels)

    if args.dag:
        extra_links = 0
        if args.dag == "sparse":
            extra_links = len(treelevels) / 2
        elif args.dag == "medium":
            extra_links = len(treelevels)
        else:
            extra_links = len(treelevels) * 2

        generate_dag(graph, extra_links, treelevels)

    if DEBUG:
        print "Graph:"
        print_graph(graph, treelevels)

    if args.image:
        graph_to_image(graph, args.image)

    mod_graph = deepcopy(graph)

    if args.swap:
        nodes_to_swap = list(mod_graph)
        shuffle(nodes_to_swap)
        if DEBUG:
            print "\nGenerating swapping mutations:"

        if args.swap > (len(nodes_to_swap) / 2):
            logging.warning("Specfied more swappings than the highest number possible for the current graph")
            args.swap = len(nodes_to_swap) / 2

        for _ in xrange(args.swap):
            source_node = nodes_to_swap.pop()
            dest_node = nodes_to_swap.pop()

            if DEBUG:
                print "  Swapping nodes ", source_node, dest_node

            swap_nodes(mod_graph, source_node, dest_node)

    if args.change:
        if DEBUG:
            print "\nGenerating external labels mutations"

        if args.change > len(graph):
            logging.warning('Requesting more changes than nodes the graph contains')
            args.change = len(graph)

        nodes_to_add = set(chain.from_iterable([list(ascii_lowercase),
                                               list(ascii_uppercase),
                                               list(digits)]))
        nodes_to_add.symmetric_difference_update(mod_graph)
        
        if len(nodes_to_add) == 0:
            nodes_to_add = set(xrange(size+1, size+1+args.change))
        nodes_to_add = list(nodes_to_add)
        shuffle(nodes_to_add)
        nodes_to_be_changed = list(mod_graph)
        shuffle(nodes_to_be_changed)

        for _ in xrange(args.change):
            node_to_be_changed = nodes_to_be_changed.pop()
            node_to_change_to = nodes_to_add.pop()

            print "Changing node:", node_to_be_changed, "for node", node_to_change_to
            change_node(mod_graph, node_to_be_changed, node_to_change_to)
            
    if args.image or args.change:
        graph_to_image(mod_graph, args.image + "-mod")

