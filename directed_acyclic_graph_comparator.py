from itertools import chain

from directed_acyclic_graph_mapper import DirectedAcyclicGraphMapper

from hypergraph import Hypergraph

from utils import stringifyGraph
from utils import t_cost_function
from utils import radix_sort_by_num_of_variables

from utils import DEBUG_MODE


class DirectedAcyclicGraphComparator:
    """
    The class perfoms the comparation between two different
    DirectedAcyclicGraphs

    To use it call the function buildHyperGraph, it will return a hypergraph
    containing the comparision between the two dags.
    """
    def __init__(self, dag1, dag2):
        """
        The first and second parameters must be DirectedAcyclicGraphs as
        specified on the file datastructures.py"
        """

        self.dag1_mapper = DirectedAcyclicGraphMapper(dag1)
        self.dag2_mapper = DirectedAcyclicGraphMapper(dag2)
        self.hypergraph = Hypergraph()

    def costAssembler(self, functions):
        pass

    def buildHyperGraph(self):
        """
        This function builds the hypergraph that will contain the comparision
        between the two dags and all its subgraphs

        The function returns a hypergraph containing the comparision between
        the two dags.
        """

        # Compute the nodes of the hypergraph by making each possible pair
        # between two differnt nodes of each graph and computing the cost
        # function.
        for n1 in self.dag1_mapper.dag.links.iterkeys():
            for n2 in self.dag2_mapper.dag.links.iterkeys():
                value = t_cost_function([n1], [n2])
                self.hypergraph.addNode((n1, n2), value)

        # In the algorithm we don't allow to compute the cost function between
        # two subgraphs with different number of variables. Here
        # we sort both sequences of subgraphs by its number of variables.
        map1_sorted_by_variables = radix_sort_by_num_of_variables(
            self.dag1_mapper.generateAllVariableMappings())
        map2_sorted_by_variables = radix_sort_by_num_of_variables(
            self.dag2_mapper.generateAllVariableMappings())

        # Thanks to its ordering coming from the Mapper class the hypergraph
        # will be built on a top down fashion.
        # map1 and map2 will always contain the name number of variables
        for map1 in chain.from_iterable(map1_sorted_by_variables):
            for map2 in chain.from_iterable(map2_sorted_by_variables):
                # This variable will contain the total coming from the
                # substituted variables
                total_from_variables = 0.0
                # The node of the hypergraph
                hypergraph_node = (map1.subgraph.root, map2.subgraph.root)
                # The cost of the node of the hypergraph
                f1 = t_cost_function([map1.subgraph.root],
                                     [map2.subgraph.root])
                # The current hyperedge, on this implementation the order
                # matters the first node will be the node acting as a root
                # and the rest the nodes that are going to be substituted
                # by variables.
                hyperedge = (hypergraph_node, ) + tuple(zip(map1.variables,
                                                            map2.variables))

                # This is for debuging pourposes
                if DEBUG_MODE:
                    print stringifyGraph(map1.graph,
                                         map1.subgraph.root,
                                         map1.variables,
                                         map1.subgraph.nodes)
                    print stringifyGraph(map2.graph,
                                         map2.subgraph.root,
                                         map2.variables,
                                         map2.subgraph.nodes)

                    print 'Hyperedge', hyperedge

                # Check if the hyperedge doesn't exist and add it
                # to the hypergrah in that case
                if not self.hypergraph.containsHyperedge(hyperedge):
                    self.hypergraph.addHyperedge(hyperedge,
                                                 (map1.subgraph,
                                                  map2.subgraph))

                # Obtain the accumulated value for the variables involved on
                # the substitution.
                for n1, n2 in zip(map1.variables, map2.variables):
                    if DEBUG_MODE:
                        print 'Querying:', n1, n2
                    total_from_variables += self.hypergraph.getNodeValue((n1,
                                                                          n2))

                # Check if with the values we have computed we have to update
                # value of the node.
                if (f1 + total_from_variables) > \
                   self.hypergraph.getNodeValue(hypergraph_node):
                    self.hypergraph.updateNode(hypergraph_node,
                                               (f1 + total_from_variables))

                if DEBUG_MODE:
                    print 'Partial graph value', f1
                    print 'Variables value', total_from_variables
                    print "=========================="

        if DEBUG_MODE:
            self.hypergraph.printNodes()
            self.hypergraph.printHyperedges()
