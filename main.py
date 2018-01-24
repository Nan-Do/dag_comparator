from collections import defaultdict

from datastructures import DirectedAcyclicGraph
# from directed_acyclic_graph_mapper import DirectedAcyclicGraphMapper
from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator

if __name__ == '__main__':
    # root = "a"
    # graph = {
    #     "a": tuple("bcd"),
    #     "b": tuple("cd"),
    #     "c": tuple("e"),
    #     "d": tuple(""),
    #     "e": tuple(""),
    #     # "c": tuple("e"),
    #     # "d": tuple("h"),
    #     # "e": tuple(""),
    #     # "f": tuple(""),
    #     # "h": tuple("")
    # }
    # dag = DirectedAcyclicGraph(root, graph)
    # dag_mapper = DirectedAcyclicGraphMapper(dag)

    # import pudb; pudb.set_trace()
    # print getSelectableNodes("ced", root, graph)
    # print dag_mapper.generateVariableMappings(dag_mapper.root, 2)
    # print dag_mapper.generateSourceSubgraphs(2)
    # dag_mapper.generateAllVariableMappings(1, 1)
    # successors = defaultdict(dict)
    # dag_mapper._DirectedAcyclicGraphMapper__buildSuccessors('b', 0, set(), successors)
    # print successors
    # dag_mapper.generateAllVariableMappings(3, 2)
    # print dag_mapper.generateSourceSubgraphs(0)

    # import pudb; pudb.set_trace()
    # SMALL SIZE
    # root = "a"
    # links = {
    #     "a": tuple("bc"),
    #     "b": tuple("d"),
    #     "c": tuple("e"),
    #     "d": tuple(""),
    #     "e": tuple("")
    # }
    # dag1 = DirectedAcyclicGraph(root, links)

    # root = "A"
    # links = {
    #     "A": tuple("BC"),
    #     "B": tuple("D"),
    #     "C": tuple(),
    #     "D": tuple()
    # }
    # dag2 = DirectedAcyclicGraph(root, links)
  
    # MEDIUM SIZE
    # root = "a"
    # links = {
    #     "a": tuple("bcd"),
    #     "b": tuple("ej"),
    #     "c": tuple("f"),
    #     "d": tuple("hi"),
    #     "e": tuple(""),
    #     "j": tuple(""),
    #     "f": tuple(""),
    #     "h": tuple(""),
    #     "i": tuple("")
    # }
    # dag1 = DirectedAcyclicGraph(root, links)

    # root = "A"
    # links = {
    #     "A": tuple("BD"),
    #     "B": tuple("CEF"),
    #     "D": tuple("HIJ"),
    #     "C": tuple(""),
    #     "E": tuple(""),
    #     "F": tuple(""),
    #     "H": tuple(""),
    #     "I": tuple(""),
    #     "J": tuple("")
    # }
    # dag2 = DirectedAcyclicGraph(root, links)
    
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

    comparator = DirectedAcyclicGraphComparator(dag1, dag2)
    comparator.buildHyperGraph()
    # comparator.hypergraph.printNodes()
    # comparator.hypergraph.printHyperedges()
    comparator.hypergraph.saveToFile("hypergraph.dat")
