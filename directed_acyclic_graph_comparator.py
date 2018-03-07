from directed_acyclic_graph_mapper import DirectedAcyclicGraphMapper

from hypergraph import Hypergraph

from utils import stringifyGraph
from utils import t_cost_edges_distance_graphs_no_vars
from utils import t_cost_edges_distance_graphs_with_vars

from utils import DEBUG_MODE


class DirectedAcyclicGraphComparator:
    """
    The class perfoms the comparation between two different
    DirectedAcyclicGraphs

    To use it call the function buildHyperGraph, it will return a hypergraph
    containing the comparision between the two dags. The contents of the
    hypergraph will be as follows:
        nodes: formed by one node of each graph storing the value of applying
               the cost function to both nodes.
        hyperedges: hyperedges are directed, the first node of the hyperedge is
                    the source node of the transformation, the rest of the
                    nodes of the hyperedges will contain the location of the
                    variables. As a value it will store the sum of the cost of
                    the variables plus applying the transformation function to
                    the graphs without the nodes being substituted. Each
                    hyperedge must be different.
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

    def __sort_by_num_of_variables(self, v):
        max_num_of_variables = max(map(lambda x: len(x.variables), v))
        answers = tuple([[] for _ in xrange(max_num_of_variables)])

        for x in v:
            answers[len(x.variables)-1].append(x)

        return answers

    def __iterate_over_sorted_maps(self, s1, s2):
        for x1, x2 in zip(s1, s2):
            for map1 in x1:
                for map2 in x2:
                    yield (map1, map2)

    def buildHyperGraph(self, number_of_variables=float('inf')):
        """
        This function builds the hypergraph that will contain the comparision
        between the two dags and all its subgraphs

        The function returns a hypergraph containing the comparision between
        the two dags.
        """

        # Compute the nodes of the hypergraph and its associated cost. Each
        # node is formed by each possible pair created using two random nodes
        # of each dag.
        g1 = self.dag1_mapper.dag
        g2 = self.dag2_mapper.dag
        for n1 in self.dag1_mapper.dag.links.iterkeys():
            for n2 in self.dag2_mapper.dag.links.iterkeys():
                # value = t_cost_function_distance([n1], [n2])
                value = t_cost_edges_distance_graphs_no_vars(g1, n1,
                                                             g2, n2)
                self.hypergraph.addNode((n1, n2), value)

        # In the algorithm we don't allow to compute the cost function between
        # two subgraphs with different number of variables. Here
        # we sort both sequences of subgraphs by its number of variables to
        # assure that doesn't happen.
        map1_sorted_by_vars = self.__sort_by_num_of_variables(
            self.dag1_mapper.generateAllVariableMappings(number_of_variables=
                                                         number_of_variables))
        map2_sorted_by_vars = self.__sort_by_num_of_variables(
            self.dag2_mapper.generateAllVariableMappings(number_of_variables=
                                                         number_of_variables))

        # Thanks to its ordering coming from the Mapper class the hypergraph
        # will be built on a top down fashion.
        # map1 and map2 will always contain the same number of variables.
        for map1, map2 in self.__iterate_over_sorted_maps(map1_sorted_by_vars,
                                                          map2_sorted_by_vars):
            # This variable will contain the total coming from the
            # substituted variables.
            # total_from_variables = 0.0

            # The node of the hypergraph.
            hypergraph_node = (map1.subgraph.root, map2.subgraph.root)

            # The current hyperedge, on this implementation the order
            # matters the first node will be the node acting as a root
            # and the rest the nodes that are going to be substituted
            # by variables.
            hyperedge = (hypergraph_node, ) + tuple(zip(map1.variables,
                                                        map2.variables))

            # The cost of the node of the hypergraph.
            # f1 = t_cost_function([map1.subgraph.root],
            #                      [map2.subgraph.root])
            weight = t_cost_edges_distance_graphs_with_vars(map1, map2)

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

            # Obtain the accumulated value for the variables involved on
            # the substitution.
            # for n1, n2 in zip(map1.variables, map2.variables):
            #     if DEBUG_MODE:
            #         print 'Querying:', n1, n2
            #     total_from_variables += self.hypergraph.getNodeWeight((n1,
            #                                                            n2))

            # Add the hyperedge to the graph
            # The hyperedges are directed and as the algorithm works
            # there should't be any duplicates so there is no need to
            # check if it exists.
            subgraphs = (map1.subgraph, map2.subgraph)
            # weight = f1 + total_from_variables
            self.hypergraph.addHyperedge(hyperedge, subgraphs, weight)

            # Check if with the values we have computed we have to update
            # value of the node.
            # if (f1 + total_from_variables) > \
            #    self.hypergraph.getNodeValue(hypergraph_node):
            #     self.hypergraph.updateNode(hypergraph_node,
            #                                (f1 + total_from_variables))

            # if DEBUG_MODE:
            #     print 'Partial graph value', f1
            #     print 'Variables value', total_from_variables
            #     print "=========================="

        if DEBUG_MODE:
            print "\nNodes:"
            print "=========================="
            self.hypergraph.printNodes()
            print "\nHyperedges:"
            print "=========================="
            self.hypergraph.printHyperedges()

    def buildHyperGraphDebug(self, number_of_variables=float('inf')):
        """
        Debugging function that uses the default computing cost function
        to build the hypergraph.

        Used for testing purposes.
        """

        for n1 in self.dag1_mapper.dag.links.iterkeys():
            for n2 in self.dag2_mapper.dag.links.iterkeys():
                value = t_cost_default([n1], [n2])
                self.hypergraph.addNode((n1, n2), value)

        map1_sorted_by_vars = self.__sort_by_num_of_variables(
            self.dag1_mapper.generateAllVariableMappings(number_of_variables=
                                                         number_of_variables))
        map2_sorted_by_vars = self.__sort_by_num_of_variables(
            self.dag2_mapper.generateAllVariableMappings(number_of_variables=
                                                         number_of_variables))

        for map1, map2 in self.__iterate_over_sorted_maps(map1_sorted_by_vars,
                                                          map2_sorted_by_vars):
            hypergraph_node = (map1.subgraph.root, map2.subgraph.root)
            hyperedge = (hypergraph_node, ) + tuple(zip(map1.variables,
                                                        map2.variables))
            weight = t_cost_default(map1.subgraph.nodes, map2.subgraph.nodes)

            subgraphs = (map1.subgraph, map2.subgraph)
            self.hypergraph.addHyperedge(hyperedge, subgraphs, weight)
