import argparse

from datetime import datetime

from datastructures import DirectedAcyclicGraph
from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator
from mappings_iterator import MappingsIterator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compute the likilyhood of two directed acyclic graphs")
    parser.add_argument("--size", dest="size",
                        default="big",
                        type=str,
                        help="Choose the size of the graphs",
                        choices=["small", "medium", "big"])
    args = parser.parse_args()

    dag1 = dag2 = None
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

    else:
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

    t1 = datetime.now()
    comparator = DirectedAcyclicGraphComparator(dag1, dag2)
    comparator.buildHyperGraph()

    best = None
    t2 = datetime.now()
    mappings = MappingsIterator(comparator.hypergraph, ('a', 'A'))
    for pos, x in enumerate(mappings):
        if pos == 0:
            best = x
        pass
    t3 = datetime.now()
    
    print "Computation finished: (" + args.size + ")"
    print " => Hypergraph nodes: ", len(comparator.hypergraph.nodes)
    print " => Hypergraph hyper-edges: ", len(comparator.hypergraph.hyperedges)
    print " => Time spent building the Hypergraph (tree-tree mapping):", str((t2 - t1).total_seconds()) + "s"
    print " =>", pos, "total mappings generated"
    print " => Total time spent generating mappings: ", str((t3 - t2).total_seconds()) + "s"
    print " => Best mapping:"
    print best
    print " => Total time spent: ", str((t3 - t1).total_seconds()) + "s"

