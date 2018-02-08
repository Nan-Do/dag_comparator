from collections import defaultdict, namedtuple
from copy import deepcopy
from itertools import chain
from random import choice, shuffle, normalvariate, randint
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits

import argparse
import logging
import sys

DEBUG = True

Position = namedtuple('Position', ['level', 'block', 'position'])
GraphLink = namedtuple('GraphLink', ['orig', 'dest'])


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


def generate_treelinks(treelevels):
    tree_links = []

    # Process the root
    root = Position(0, 0, 0)
    for block, b in enumerate(treelevels[1]):
        for position, x in enumerate(b):
            dest = Position(1, block, position)
            tree_links.append(GraphLink(root, dest))

    for level, (x, y) in enumerate(get_chunks(treelevels[1:], 2), start=1):
        election_positions = []
        for block, b in enumerate(x):
            for position, _ in enumerate(b):
                election_positions.append(Position(level, block, position))
        shuffle(election_positions)

        for dest_block, block in enumerate(y):
            if not election_positions:
                logging.error("The tree levels are not normalized")
                sys.exit(0)

            orig_position = election_positions.pop()
            for dest_position, node in enumerate(block):
                dest_position = Position(level + 1,
                                         dest_block,
                                         dest_position)
                tree_links.append(GraphLink(orig_position,
                                            dest_position))

    return tree_links


def generate_graph(treelevels, treelinks):
    graph = defaultdict(list)

    for node in chain.from_iterable(chain.from_iterable(treelevels)):
        graph[node]

    for link in treelinks:
        orig_position, dest_position = link

        level, block, position = orig_position
        orig_node = treelevels[level][block][position]

        level, block, position = dest_position
        dest_node = treelevels[level][block][position]

        graph[orig_node].append(dest_node)

    return graph


def generate_dag(num_of_links, treelevels, treelinks):
    total = 0
    while num_of_links > 0:
        total += 1
        if total == 100:
            logging.warning("Unable to generate a DAG using the current tree")
            return
        # Get the source node
        source_level = randint(0, len(treelevels) - 2)
        source_block = randint(0, len(treelevels[source_level]) - 1)
        source_position = randint(0, len(treelevels[source_level][source_block]) - 1)

        # Get the destination node
        dest_level = randint(source_level + 1, len(treelevels) - 1)
        dest_block = randint(0, len(treelevels[dest_level]) - 1)
        dest_position = randint(0, len(treelevels[dest_level][dest_block]) - 1)

        # if dest_level == source_level + 1:
        #     continue

        graph_link = GraphLink(Position(source_level,
                                        source_block,
                                        source_position),
                               Position(dest_level,
                                        dest_block,
                                        dest_position))
        # Check that the link doestn't exist already
        if graph_link in treelinks:
            continue

        treelinks.append(graph_link)
        num_of_links -= 1

def generate_dot(treelevels, treelinks, fname):
    with open(fname + '.dot', 'w') as f:
        f.write('strict digraph {\n')
        for link in treelinks:
            orig_position, dest_position = link

            level, block, position = orig_position
            orig_node = treelevels[level][block][position]

            level, block, position = dest_position
            dest_node = treelevels[level][block][position]

            f.write('\t{} -> {};\n'.format(orig_node,
                                           dest_node))

        f.write('}')


def swap_nodes_mutation(treelevels, orig_node, dest_node):
    for level in treelevels:
        for block in level:
            if orig_node in block and dest_node in block:
                a = block.index(orig_node)
                b = block.index(dest_node)
                block[a], block[b] = block[b], block[a]
            elif orig_node in block:
                index = block.index(orig_node)
                block[index] = dest_node
            elif dest_node in block:
                index = block.index(dest_node)
                block[index] = orig_node


def relabel_node_mutation(treelevels, node_to_be_changed, node_to_change_to):
    for level in treelevels:
        for block in level:
            if node_to_be_changed in block:
                index = block.index(node_to_be_changed)
                block[index] = node_to_change_to


def delete_branch_mutation(treelevels, treelinks, start_from_root=False):
    if not treelinks:
        logging.warning("No more branchs to delete")
        return

    orig_link = choice(treelinks)
    if start_from_root:
        root = Position(0, 0, 0)
        orig_link = choice(filter(lambda x: x.orig == root,
                                  treelinks))

    frontier = [orig_link]
    print "Removing branch:"
    while frontier:
        link = frontier.pop()
        treelinks.remove(link)

        orig = link.orig
        dest = link.dest
        orig_node = treelevels[orig.level][orig.block][orig.position]
        dest_node = treelevels[dest.level][dest.block][dest.position]
        
        print "Removing link from node ", orig_node, "to", dest_node

        # There is still a path that can reach the current dest node
        # no need to remove its descecndants
        if filter(lambda x: x.dest == dest, treelinks):
            continue

        # Get all the links that start on the dest node
        links = filter(lambda x: x.orig == dest, treelinks)
        
        frontier.extend(links)


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
                        help="Mutation that swaps two nodes. This operation is repeated SWAP times")

    parser.add_argument("--relabel", dest="relabel",
                        type=int,
                        help="Mutation that relabels one node with a label from outside the domain. This operation is repeated RELABEL times")

    parser.add_argument("--delete", dest="delete",
                        type=int,
                        help="Mutation that deletes a branch. This operation is repeated DELETE times")

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

    treelinks = generate_treelinks(treelevels)
    if DEBUG:
        print "Graph:"
        print treelevels, treelinks
        # print_graph(graph, treelevels)

    if args.dag:
        extra_links = 0
        if args.dag == "sparse":
            extra_links = len(treelevels) / 2
        elif args.dag == "medium":
            extra_links = len(treelevels)
        else:
            extra_links = len(treelevels) * 2

        generate_dag(extra_links, treelevels, treelinks)

    mod_treelevels = deepcopy(treelevels)
    mod_treelinks = deepcopy(treelinks)

    if args.swap:
        nodes = list(chain.from_iterable(chain.from_iterable(mod_treelevels)))
        shuffle(nodes)
        if DEBUG:
            print "\nSwapping mutations:"

        if args.swap > (len(nodes) / 2):
            logging.warning("Specfied more swappings than the highest number possible for the current graph")
            args.swap = len(nodes) / 2

        for _ in xrange(args.swap):
            source_node = nodes.pop()
            dest_node = nodes.pop()

            if DEBUG:
                print "  Swapping nodes ", source_node, dest_node

            swap_nodes_mutation(mod_treelevels,
                                source_node,
                                dest_node)

    if args.relabel:
        nodes = list(chain.from_iterable(chain.from_iterable(mod_treelevels)))
        if DEBUG:
            print "\nRelabeling mutations:"

        if args.relabel > len(nodes):
            logging.warning('Requesting more changes than nodes the graph contains')
            args.relabel = len(nodes)

        nodes_to_add = set(chain.from_iterable([list(ascii_lowercase),
                                               list(ascii_uppercase),
                                               list(digits)]))
        nodes_to_add.symmetric_difference_update(nodes)

        if len(nodes_to_add) == 0:
            nodes_to_add = set(xrange(size+1, size+1+args.change))
        nodes_to_add = list(nodes_to_add)
        shuffle(nodes_to_add)
        nodes_to_be_changed = nodes
        shuffle(nodes_to_be_changed)

        for _ in xrange(args.relabel):
            node_to_be_changed = nodes_to_be_changed.pop()
            node_to_change_to = nodes_to_add.pop()

            print "Changing node:", node_to_be_changed, "for node", node_to_change_to
            relabel_node_mutation(mod_treelevels,
                                  node_to_be_changed,
                                  node_to_change_to)

    if args.delete:
        for _ in xrange(args.delete):
            delete_branch_mutation(mod_treelevels,
                                   mod_treelinks)

    # graph = generate_graph(treelevels, treelinks)
    generate_dot(treelevels, treelinks, 'test')
    generate_dot(mod_treelevels, mod_treelinks, 'test-mod')
