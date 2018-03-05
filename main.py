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
        root = "a"
        links = {
            "a": tuple("bc"),
            "b": tuple("d"),
            "c": tuple("e"),
            "d": tuple(""),
            "e": tuple("")
        }
        dag1 = DirectedAcyclicGraph(root, links, dict())

        root = "A"
        links = {
            "A": tuple("BC"),
            "B": tuple("D"),
            "C": tuple(),
            "D": tuple()
        }
        dag2 = DirectedAcyclicGraph(root, links, dict())

    elif args.size == "medium":
        # MEDIUM SIZE
        root = "a"
        links = {
            "a": tuple("bcd"),
            "b": tuple("ej"),
            "c": tuple("f"),
            "d": tuple("hi"),
            "e": tuple(""),
            "j": tuple(""),
            "f": tuple(""),
            "h": tuple(""),
            "i": tuple("")
        }
        dag1 = DirectedAcyclicGraph(root, links, dict())

        root = "A"
        links = {
            "A": tuple("BD"),
            "B": tuple("CEF"),
            "D": tuple("HIJ"),
            "C": tuple(""),
            "E": tuple(""),
            "F": tuple(""),
            "H": tuple(""),
            "I": tuple(""),
            "J": tuple("")
        }
        dag2 = DirectedAcyclicGraph(root, links, dict())

    elif args.size == "big":
        # BIG SIZE
        root = "a"
        links = {
            "a": tuple("bcd"),
            "b": tuple("ej"),
            "c": tuple("f"),
            "d": tuple("hi"),
            "e": tuple("qgs"),
            "f": tuple("z"),
            "g": tuple(""),
            "h": tuple("rtu"),
            "i": tuple("wx"),
            "j": tuple("kl"),
            "k": tuple("mn"),
            "l": tuple("y"),
            "m": tuple(""),
            "n": tuple(""),
            "o": tuple(""),
            "p": tuple(""),
            "q": tuple(""),
            "r": tuple(""),
            "s": tuple(""),
            "t": tuple("vop"),
            "u": tuple(""),
            "v": tuple(""),
            "w": tuple(""),
            "x": tuple(""),
            "y": tuple(""),
            "z": tuple("")
        }
        dag1 = DirectedAcyclicGraph(root, links, dict())

        root = "A"
        links = {
            "A": tuple("BD"),
            "B": tuple("CEF"),
            "C": tuple("KGL"),
            "D": tuple("HIJ"),
            "E": tuple("MN"),
            "F": tuple("Z"),
            "G": tuple(""),
            "H": tuple("RTU"),
            "I": tuple("WX"),
            "J": tuple("YOQ"),
            "K": tuple("PSV"),
            "L": tuple(""),
            "M": tuple(""),
            "N": tuple(""),
            "O": tuple(""),
            "P": tuple(""),
            "Q": tuple(""),
            "R": tuple(""),
            "S": tuple(""),
            "T": tuple(""),
            "U": tuple(""),
            "V": tuple(""),
            "W": tuple(""),
            "X": tuple(""),
            "Y": tuple(""),
            "Z": tuple("")
        }
        dag2 = DirectedAcyclicGraph(root, links, dict())

    compute_just_best = True
    if args.size:
        compute_just_best = False

    # Perform the execution
    comparator, best, total_transitions, t1, t2, t3 = \
        perform_execution(dag1, dag2, num_of_vars, compute_just_best)

    # Print the statistics and related information to the computation
    print_info(comparator, best, total_transitions, t1, t2, t3)
