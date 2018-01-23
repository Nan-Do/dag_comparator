from compute_best_mappings import ComputeBestKMappings
from collections import defaultdict, namedtuple
import cPickle as pickle

from utils import DEBUG_MODE

NodeData = namedtuple("NodeData", ["weight", "hyperedges"])
HyperedgeLabel = namedtuple("HyperedgeLabel", ["subgraphs", "weight"])


class Hypergraph:
    """
    This class represents  a simple hypergraph
    It functions by specifying the nodes that forms the hypergraph and
    then the edges.
    So far it is quite simple and only adding functions have been
    implemented but the algorithim doesn't require to remove any data
    Both the nodes and the hyperedges can be labeled with data.
    """

    def __init__(self):
        self.last_hyperedge = 0
        self.nodes = defaultdict(NodeData)
        self.hyperedges = dict()
        self.positions_to_hyperedges = dict()

    def addNode(self, node, weight):
        """
        This function adds a node to the hypergraph.
        If the node already exists it raises an exeception.
        Node -> The node of the hypergraph must be inmutable.
        Weight -> The weight associated with the node.
        """
        if node not in self.nodes:
            self.nodes[node] = NodeData(weight, list())
        else:
            raise ValueError("The node already exists on the hypergraph")

    def updateNode(self, node, weight):
        """
        This functions updates the weight associated with a node of
        the hypergraph. If the node doesn't exists raises an exception
        Node -> The node of the hypergraph must be inmutable.
        Weight -> The weight associated with the node.
        """
        if node not in self.nodes:
            raise ValueError("The node doesn't exists on the hypergraph")

        self.nodes[node].weight = weight

    def containsNode(self, node):
        """
        This function checks if the node exist on the hypergraph.
        Node -> The node of the hypergraph must be inmutable.
        """
        return node in self.nodes

    def getNodeWeight(self, node):
        """
        This function returns the weight associated with a node. If the node
        doesn't exists raises an exception
        Node -> The node of the hypergraph must be inmutable.
        """
        if node not in self.nodes:
            raise ValueError("The node doesn't exists on the hypergraph")

        return self.nodes[node].weight

    def addHyperedge(self, hyperedge, subgraphs, weight):
        """
        This function adds a hyperedges to the hypergraph. If it already exists
        it raises an exception.
        hyperedge -> a tuple of nodes if a node doesn't exists it raises an
                     exception.
        subgraphs -> must be a tuple of two DirectedAcyclicGraphs
        weight -> the weight of the hyperedge
        """
        if hyperedge not in self.hyperedges:
            current_position = self.last_hyperedge
            self.last_hyperedge += 1

            for node in hyperedge:
                if node not in self.nodes:
                    raise ValueError("The hyperedge contains a node that " +
                                     "doesn't exist on the hypergraph")

                self.nodes[node].hyperedges.append(current_position)

            self.positions_to_hyperedges[current_position] = hyperedge
        else:
            raise ValueError("The hyperedge already exists on the hypergraph")

        self.hyperedges[hyperedge] = HyperedgeLabel(subgraphs, weight)

    def containsHyperedge(self, hyperedge):
        """
        This function checks if the hyperedge exist on the hypergraph.
        hyperedge -> a tuple of nodes if a node doesn't exists it raises an
                     exception.
        """
        return hyperedge in self.hyperedges

    def getHyperedgeLabel(self, hyperedge):
        """
        This function returns the label associated with a hyperedge of the
        hyperedge. If it doesn't exists it raises an exception
        hyperedges -> a tuple of nodes if a node doesn't exists it raises an
                      exception.
        """
        if hyperedge not in self.hyperedges:
            raise ValueError("The hyperedge doesn't exists on the hypergraph")

        return self.hyperedges[hyperedge]

    def updateHyperedgeLabel(self, hyperedge, subgraphs, weight):
        """
        This function updates the label associated with a hyperedge of the
        hyperedge. If it doesn't exists it raises an exception
        hyperedge -> a tuple of nodes if a node doesn't exists it raises an
                     exception.
        subgraphs -> must be a tuple of two DirectedAcyclicGraphs
        weight -> the weight of the hyperedge
        """
        if hyperedge not in self.hyperedges:
            raise ValueError("The hyperedge doesn't exists on the hypergraph")

        self.hyperedges[hyperedge] = HyperedgeLabel(subgraphs, weight)

    def getHyperedgesFromNode(self, node):
        """
        This function returns the hyperedges that a node belongs to. If the
        node doesn't exist on the hypergraph it raises an exception.
        """
        if node not in self.nodes:
            raise ValueError("The node doesn't exists on the hypergraph")

        hyperedges = list()
        for hyperedge_position in self.nodes[node].hyperedges:
            hyperedges.append(self.positions_to_hyperedges[hyperedge_position])

        return hyperedges

    def printNodes(self):
        i = 1
        for node, v in self.nodes.iteritems():
            print i, node, v.weight
            i += 1

    def printHyperedges(self):
        i = 1
        for hyperedge, label in self.hyperedges.iteritems():
            print i, hyperedge, label.weight
            if DEBUG_MODE:
                print "   ", label.subgraphs[0]
                print "   ", label.subgraphs[1]

            i += 1

    def saveToFile(self, filename):
        f = file(filename, "w+")
        pickle.dump(self, f)
        f.close()

    @staticmethod
    def loadFromFile(filename):
        f = file(filename, "r")
        hypergraph = pickle.load(f)
        f.close()
        return hypergraph

if __name__ == '__main__':
    h = Hypergraph.loadFromFile('hypergraph.dat')
    h.printNodes()
    x = ComputeBestKMappings(h, ('a', 'A'))
