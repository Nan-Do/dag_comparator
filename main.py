import argparse
import sys
import os.path

from datetime import datetime

from datastructures import DirectedAcyclicGraph
from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator
from mappings_iterator import MappingsIterator
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
    print " => Total time spent generating mappings: ", \
          str((t3 - t2).total_seconds()) + "s"
    print " => Best mapping:"
    print best
    print " => Best score:", compute_best_score(best)
    print " => Total time spent: ", str((t3 - t1).total_seconds()) + "s"


def perform_execution(dag1, dag2, just_best_mapping=True):
    # Build the hypergraph
    t1 = datetime.now()
    comparator = DirectedAcyclicGraphComparator(dag1, dag2)
    comparator.buildHyperGraph()

    # Enumerate all the possible mappings
    best = None
    t2 = datetime.now()
    mappings = MappingsIterator(comparator.hypergraph, (dag1.root, dag2.root))
    for pos in count(start=1):
        if pos == 1:
            best = mappings.next()
            if just_best_mapping:
                break
        else:
            try:
                mappings.next(False)
            except StopIteration:
                break
    t3 = datetime.now()

    return comparator, best, t1, t2, t3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compute the likelihood" +
                                     " of two directed acyclic graphs")
    parser.add_argument("--size", dest="size",
                        type=str,
                        help="Choose the size of the sample graphs (not " +
                             "compatible with the dag options)",
                        choices=["small", "medium", "big"])

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

    print args.dag1, args.dag2
    if (args.dag1 or args.dag2) and args.size:
        print "Error::Specified both the sample graph and source files " +\
              "for them."
        sys.exit(0)

    if (args.dag1 and not args.dag2) or (not args.dag1 and args.dag2):
        print "Error::Both source files must be specified in order to " +\
              "perform the analysis"

    if args.dag1:
        path, fname = os.path.split(args.dag1)
        fname = fname.split('.')[0]
        sys.path.append(path)
        d = __import__(fname)
        dag1 = DirectedAcyclicGraph(d.root, d.links)

    if args.dag2:
        path, fname = os.path.split(args.dag2)
        fname = fname.split('.')[0]
        sys.path.append(path)
        d = __import__(fname)
        dag2 = DirectedAcyclicGraph(d.root, d.links)

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
        dag1 = DirectedAcyclicGraph(root, links)

        root = "A"
        links = {
            "A": tuple("BC"),
            "B": tuple("D"),
            "C": tuple(),
            "D": tuple()
        }
        dag2 = DirectedAcyclicGraph(root, links)

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
        dag1 = DirectedAcyclicGraph(root, links)

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
        dag2 = DirectedAcyclicGraph(root, links)

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
        dag1 = DirectedAcyclicGraph(root, links)

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
        dag2 = DirectedAcyclicGraph(root, links)

    compute_just_best = True
    if args.size:
        compute_just_best = False

    # Perform the execution
    comparator, best, total_transitions, t1, t2, t3 = \
        perform_execution(dag1, dag2, compute_just_best)

    # Print the statistics and related information to the computation
    print_info(comparator, best, t1, t2, t3)
