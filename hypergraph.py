from collections import defaultdict


class NodeData:
    def __init__(self, value, hyperedges):
        self.value = value
        self.hyperedges = hyperedges


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

    def addNode(self, node, value):
        """
        This function adds a node to the hypergraph.
        If the node already exists it updates its value
        Node -> The node of the hypergraph must be inmutable.
        Value -> The value associated with the node.
        """
        if node not in self.nodes:
            self.nodes[node] = NodeData(value, list())
        else:
            self.nodes[node].value = value

    def updateNode(self, node, value):
        """
        This functions updates the value associated with a node of
        the hypergraph. If the node doesn't exists raises an exception
        Node -> The node of the hypergraph must be inmutable.
        Value -> The value associated with the node.
        """
        if node not in self.nodes:
            raise ValueError("The node doesn't exists on the hypergraph")

        self.nodes[node].value = value

    def getNodeValue(self, node):
        """
        This function returns the value associated with a node. If the node
        doesn't exists raises an exception
        Node -> The node of the hypergraph must be inmutable.
        Value -> The value associated with the node.
        """
        if node not in self.nodes:
            raise ValueError("The node doesn't exists on the hypergraph")

        return self.nodes[node].value

    def addHyperedge(self, hyperedge, label):
        """
        This function adds a hyperedges to the hypergraph. If it already exists
        it updates its associated label.
        hyperedges -> a tuple of nodes if a node doesn't exists it raises an
                      exception.
        label -> The data associated with the hyperedges.
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

        self.hyperedges[hyperedge] = label

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

    def updateHyperedgeLabel(self, hyperedge, label):
        """
        This function updates the label associated with a hyperedge of the
        hyperedge. If it doesn't exists it raises an exception
        hyperedges -> a tuple of nodes if a node doesn't exists it raises an
                      exception.
        """
        if hyperedge not in self.hyperedges:
            raise ValueError("The hyperedge doesn't exists on the hypergraph")

        self.hyperedges[hyperedge] = label

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
