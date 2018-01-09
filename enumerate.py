from directed_acyclic_graph DirectedAcyclicGraphMapper

if __name__ == '__main__':
    root = "a"
    graph = {
        "a": tuple("bcd"),
        "b": tuple("cd"),
        "c": tuple("e"),
        "d": tuple(""),
        "e": tuple(""),
        # "c": tuple("e"),
        # "d": tuple("h"),
        # "e": tuple(""),
        # "f": tuple(""),
        # "h": tuple("")
    }
    dag = DirectedAcyclicGraphMapper(graph)

    # import pudb; pudb.set_trace()
    # print getSelectableNodes("ced", root, graph)
    # print dag.generateVariableCombinations(dag.root, 2)
    # print dag.generateSourceSubgraphs(2)
    dag.generateAllVariableCombinations(1, 1)
    # print stringifyGraph(root, graph, "a")
    # successors = defaultdict(tuple)
    # BuildSuccessors(root, graph, set(), successors)
    # print successors
    # print map(sorted, generateSubGraphsDagWithRoot(root, graph))
