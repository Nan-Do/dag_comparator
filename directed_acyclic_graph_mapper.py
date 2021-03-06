from collections import defaultdict, deque

from datastructures import DirectedAcyclicSubgraph
from datastructures import DirectedAcyclicSubgraphWithVariables
from utils import stringifyGraph


class DirectedAcyclicGraphMapper:
    """
    This class takes a Direct acyclic graph and computes all its possible
    mappings.

    The dag is a Directed Acyclic Graph as specified in the file datastructures.
    To generate all the possible variable mappings the function
    generateAllVariableCombinations has to be used
    """

    def __init__(self, dag):
        self.dag = dag

    # TODO: Currently a recursive version, create the iterative version
    def __buildSuccessors(self, node, depth, antecessors, successors):
        """
        Auxiliary recursive function that compute all the possible successors
        of a node in a graph indicating also its minimum distance. The function
        does the  same recursively for all its descendants.
        Input:
         node: The node from which we want to compute the successors.
         depth: The current depth of the recursion it must start on 0.
         antecessor: The set of antecessors of the current node. The first call
                     must use an empty set.
         successors: A dictionary of dictionaries, it will contain the successors
                     and the minimum distance to each one from the root.
                     This parameter will also be the output. The dictionary is
                     mutated on place so the paramater is a referece. The first
                     call must use an empty defaultdict(dict).
        Ex: For the graph
              a
             / \
             b c
        It will return on successors
        defaultdict(<type 'dict'>, {'a': {'c': 1, 'b': 1}})
        """

        for antecessor in antecessors:
            temp_dict = successors[antecessor]
            if node not in temp_dict:
                temp_dict[node] = depth
            else:
                if depth < temp_dict[node]:
                    temp_dict[node] = depth

        next_antecessors = antecessors.union(node)
        for child in self.dag.links[node]:
            self.__buildSuccessors(child,
                                   depth + 1,
                                   next_antecessors,
                                   successors)

    def __get_minimum_distance_from_root(self, node, successors):
        """
        This functions returns the minium distance between a node and the root
        of the dag.

        The distances are precomputed on the successors param
        """
        if node == self.dag.root:
            return 0

        if node in successors[self.dag.root]:
            return successors[self.dag.root][node]

        return -1

    def generateSourceSubgraphs(self, max_depth=float("inf")):
        """
        This function generates all the source subgraphs required to put all
        the mapping variables. As input it takes the maximum depth that we are
        going to use to explore the graph. As an output it generates tuples of
        nodes, this tuples of nodes represent the the source subgraphs, the
        edges are the same as in the original graph so we don't need to store
        them again.

        The set of source subgraphs is the minimum set of subgraphs we require
        in order to generate all the subgraphs with variables. This means that
        is a subgraphs is subsumed into another one, for example [a, b, d] and
        [a, b], and we produce both, at the moment of generating the subgraphs
        with variables we will have duplicates. The source graphs for DAGS are
        formed by the complete graph originated by the root node and the
        subgraphs formed by its children using the children node as the root
        for the new subgraph.

        Due to the requirements of the algorithm the subgraphs must be returned
        in an ascending order from the leafs.

        Ex:
               a
              / \
              b c
              | |
              d e
        Returns:
           [d]
           [e]
           [b, d]
           [c, e]
           [a, b, c, d, e]
        """

        # Check that the provided depth is a positive integer
        if max_depth < 0:
            raise ValueError("The depth has to be a positive integer")

        # We need a set as in a DAG one node can be reached by more than one
        # path and therefore there could be duplicates, using a set avoid that.
        solutions = deque()
        frontier = deque()
        processed_roots = set()
        successors = defaultdict(dict)

        self.__buildSuccessors(self.dag.root, 0, set(), successors)

        frontier.append((self.dag.root, 0))
        while len(frontier):
            node, depth = frontier.popleft()
            # If the current depth is bigger than the minimum length required
            # to reach it from the root we are dealing with an alternative
            # longer path that can lead to incorrect answers so just skip it.
            if depth > self.__get_minimum_distance_from_root(node, successors)\
               or node in processed_roots:
                continue
            # Get the nodes that are below the requested depth
            nodes = tuple()
            if successors[node]:
                node_successors = successors[node]
                nodes = filter(lambda x: (node_successors[x] - depth) <= max_depth,
                               node_successors.iterkeys())

            if node not in processed_roots:
                subgraph = DirectedAcyclicSubgraph(node, ((node,) +
                                                          tuple(nodes)))
                solutions.appendleft(subgraph)
                processed_roots.add(node)
            depth += 1

            for child in self.dag.links[node]:
                frontier.append((child, depth))

        return solutions

    def __getSelectableNodes(self, available_nodes):
        """
        This functions computes all the possible paths of the graph
        starting from the root and using only the nodes in available_nodes.
        The function returns a set with the reachable nodes.

        Auxiliary function used to compute all the valid positions
        in which we can put a variable.

        Ex:
           ---a
          |  / \
          |  b-c
          |  | |
           --d e
        Available nodes: "cde"
        Output: set(['d', 'e', 'c'])
        """

        reachable = set()

        frontier = list(self.dag.links[self.dag.root])
        while frontier:
            node = frontier.pop()

            if node not in available_nodes:
                continue

            reachable.add(node)
            frontier.extend(self.dag.links[node])

        return reachable

    def generateVariableMappings(self,
                                 starting_node,
                                 total_number_of_variables,
                                 initial_nodes=None):
        """
        This function computes all the valid variable positions for a given
        graph. As input it takes the starting node and the total number of
        variables to set.
        As an output it returns a list of tuples, each tuple is a sequence of
        nodes, each one representing a valid position for a variable,
        initial_nodes is an optional parameter that represent the initial set
        of nodes that we will consider.  This, along the starting node, allows
        us to consider subgraphs using only a set of nodes to represent it.
        """

        solutions = set()

        # Errors
        # Incorrect number of variables
        if total_number_of_variables <= 0:
            raise ValueError("Incorrect number of variables to assign")
        # Root not belonging to the graph
        if starting_node not in self.dag.links:
            raise ValueError("The root does not belong to the graph")

        if initial_nodes is None:
            initial_nodes = set(self.dag.links.iterkeys())
        else:
            initial_nodes = set(initial_nodes)

        # The frontier is a tuple of 3 elements as follows:
        #  A set of nodes representing valid positions for the variables.
        #  A node that represents the father of the last processed node.
        #  A tuple representing where the variables have been set for the
        #  current configuration.
        frontier = [(initial_nodes.difference(starting_node),
                     starting_node,
                     tuple())]
        while frontier:
            selectable, father, variables = frontier.pop()

            if len(variables) < total_number_of_variables:
                for node in selectable:
                    # Get the nodes in which we can put a variable
                    new_selectable = \
                            self.__getSelectableNodes(selectable.difference(node))
                    solution = variables + (node,)
                    # To store all the possible permutations and not just a
                    # canonical combination change solutions to a list and
                    # do not sort the tuple
                    solutions.add(tuple(sorted(solution)))

                    # If we don't have any selectable node or the current node
                    # is not a direct children of the previous father do not
                    # process it. If we don't stop the recursion by controlling
                    # the father we get incorrect solutions.
                    if not len(new_selectable) or \
                       node not in self.dag.links[father]:
                        continue

                    frontier.append((new_selectable,
                                     father,
                                     solution))

        return solutions

    def generateAllVariableMappings(self,
                                    number_of_variables=float("inf"),
                                    max_depth=float("inf"),
                                    printMapppings=False):
        """
        This function generates all possible variable mappings for all
        the source subgraphs that can be generated for the dag.
        As input it takes the maximum number of variables to set on each
        subgraph and the max_depth to go down on each subgraph, this parameter
        is optional and by default it explores the hole graph.
        To generate the source subgraphs it calls the function
        generateSourceSubgraphs and to generate all the possible mapping for
        each source subgraph it calls the function generateVariableMappings
        """

        # Store the solutions
        solutions = list()

        # Get the source subgraphs
        source_subgraphs = self.generateSourceSubgraphs(max_depth)

        # For each subgraph get all valid combination of variables that we
        # can set up to number_of_variables
        for subgraph in source_subgraphs:
            # print source_subgraph, source_root
            # If the graph is composed by just one node it doesn't
            # return anything
            for variables in self.generateVariableMappings(subgraph.root,
                                                           number_of_variables,
                                                           subgraph.nodes):
                # Print the string version of the graph
                if printMapppings:
                    print stringifyGraph(self.dag,
                                         subgraph.root,
                                         variables,
                                         subgraph.nodes)

                solutions.append(DirectedAcyclicSubgraphWithVariables(self.dag,
                                                                      subgraph,
                                                                      variables))

        return solutions
