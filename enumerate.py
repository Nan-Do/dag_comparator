from directed_acyclic_graph import DirectedAcyclicGraph

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
    dag = DirectedAcyclicGraph(root, graph)

    # import pudb; pudb.set_trace()
    # print getSelectableNodes("ced", root, graph)
    # print dag.generateVariableCombinations(dag.root, 2)
    # print dag.generateSourceSubgraphs(2)
    dag.generateVariableMappings(1, 1)
    # print stringifyGraph(root, graph, "a")
    # successors = defaultdict(tuple)
    # BuildSuccessors(root, graph, set(), successors)
    # print successors
    # print map(sorted, generateSubGraphsDagWithRoot(root, graph))
