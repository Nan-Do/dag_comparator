from directed_acyclic_graph_mapper import DirectedAcyclicGraphMapper

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
    dag_mapper = DirectedAcyclicGraphMapper(root, graph)

    # import pudb; pudb.set_trace()
    # print getSelectableNodes("ced", root, graph)
    # print dag_mapper.generateVariableCombinations(dag_mapper.root, 2)
    # print dag_mapper.generateSourceSubgraphs(2)
    dag_mapper.generateAllVariableCombinations(1, 1)
    # print stringifyGraph(root, graph, "a")
    # successors = defaultdict(tuple)
    # BuildSuccessors(root, graph, set(), successors)
    # print successors
    # print map(sorted, generateSubGraphsDagWithRoot(root, graph))
