import argparse
import sys
import os.path

from datetime import datetime

from datastructures import DirectedAcyclicGraph
from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator
from transitions_iterator import TransitionsIterator
from itertools import count

from utils import DEBUG_MODE


def compute_best_score(best_derivation):
    b = best_derivation[0]
    score = b[1] + sum(map(lambda x: x[1], b[0]))

    return score


def print_info(comparator, best, total_transitions, t1, t2, t3):
    if DEBUG_MODE:
        print "\n"

    print "Computation finished:" 
    print " => Hypergraph nodes: ", len(comparator.hypergraph.nodes)
    print " => Hypergraph hyper-edges: ", len(comparator.hypergraph.hyperedges)
    print " => Time spent building the Hypergraph (dag-dag mapping):", \
          str((t2 - t1).total_seconds()) + "s"
    if total_transitions:
        print " =>", total_transitions, "total transitions generated"
    print " => Total time spent generating transitions: ", \
          str((t3 - t2).total_seconds()) + "s"
    print " => Best transition:"
    print best
    print " => Best score:", compute_best_score(best)
    print " => Total time spent: ", str((t3 - t1).total_seconds()) + "s"


def perform_execution(dag1, dag2, number_of_variables, just_best_mapping=True):
    total_transitions = 0

    # Build the hypergraph
    t1 = datetime.now()
    comparator = DirectedAcyclicGraphComparator(dag1, dag2)
    comparator.buildHyperGraph(number_of_variables)

    # Enumerate all the possible transitions
    best = None
    t2 = datetime.now()
    transitions = TransitionsIterator(comparator.hypergraph, (dag1.root, dag2.root))
    for pos in count(start=1):
        if pos == 1:
            best = transitions.next()
            if just_best_mapping:
                break
        else:
            try:
                transitions.next(False)
            except StopIteration:
                break
    t3 = datetime.now()

    if not just_best_mapping:
        total_transitions = pos

    return comparator, best, total_transitions, t1, t2, t3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compute the likelihood" +
                                     " of two directed acyclic graphs")
    parser.add_argument("--size", dest="size",
                        type=str,
                        help="Choose the size of the sample graphs (not " +
                             "compatible with the dag options)",
                        choices=["small", "medium", "big"])

    parser.add_argument("--variables", dest="variables",
                        type=int,
                        default=10,
                        help="Choose the maximum number of variables " +
                             "(10 by default if the number is negative as" +
                             "many variabes as possible)")

    parser.add_argument("--dag1", dest="dag1",
                        type=str,
                        help="Specify the file that contains the data for" +
                             " the first dag")

    parser.add_argument("--dag2", dest="dag2",
                        type=str,
                        help="Specify the file that contains the data for " +
                             "the second dag")

    args = parser.parse_args()

    dag1 = dag2 = None

    if not((args.dag1 and args.dag2) or args.size):
        print "Error::One method to load/generate the graphs must be specified"
        sys.exit(0)

    if (args.dag1 or args.dag2) and args.size:
        print "Error::Specified both the sample graph and source files " +\
              "for them."
        sys.exit(0)

    if (args.dag1 and not args.dag2) or (not args.dag1 and args.dag2):
        print "Error::Both source files must be specified in order to " +\
              "perform the analysis"

    num_of_vars = 10
    if args.variables:
        if args.variables < 0:
            num_of_vars = float('inf')
        else:
            num_of_vars = args.variables

    if args.dag1:
        path, fname = os.path.split(args.dag1)
        fname = fname.split('.')[0]
        sys.path.append(path)
        d = __import__(fname)
        dag1 = DirectedAcyclicGraph(d.root, d.links, d.labels)

    if args.dag2:
        path, fname = os.path.split(args.dag2)
        fname = fname.split('.')[0]
        sys.path.append(path)
        d = __import__(fname)
        dag2 = DirectedAcyclicGraph(d.root, d.links, d.labels)

    if args.size == "small":
        # SMALL SIZE
        root = 'x'
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
        dag1 = DirectedAcyclicGraph(root, links, link_labels)
        root = 'a'
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
        dag2 = DirectedAcyclicGraph(root, links, link_labels)

    elif args.size == "medium":
        # MEDIUM SIZE
        root = 'w'
        links = {
                 'w': ['b', 'r', 'W'],
                 'b': ['B'],
                 'r': ['Z', 'g', 'n'],
                 'g': ['G'],
                 'n': ['H'],
                 'W': [],
                 'B': [],
                 'G': [],
                 'Z': [],
                 'H': [],
                 }
        link_labels = {
               'A0': set([('w', 'b'), ('r', 'g')]),
               'A1': set([('w', 'r'), ('r', 'n')]),
               'I': set([('w', 'W'), ('b', 'B'), ('g', 'G'),
                         ('n', 'H'), ('r', 'Z')])
        }
        dag1 = DirectedAcyclicGraph(root, links, link_labels)
        root = 'w'
        links = {
                 'w': ['R', 'h', 'd'],
                 'h': ['J'],
                 'd': ['B'],
                 'R': [],
                 'J': [],
                 'B': [],
                 }
        link_labels = {
               'mod': set([('w', 'h')]),
               'domain': set([('w', 'd')]),
               'I': set([('w', 'R'), ('h', 'H'), ('d', 'B')])
        }
        dag2 = DirectedAcyclicGraph(root, links, link_labels)

    elif args.size == "big":
        # BIG SIZE
        raise NotImplementedError

    compute_just_best = True
    if args.size:
        compute_just_best = False

    # Perform the execution
    comparator, best, total_transitions, t1, t2, t3 = \
        perform_execution(dag1, dag2, num_of_vars, compute_just_best)

    # Print the statistics and related information to the computation
    print_info(comparator, best, total_transitions, t1, t2, t3)
