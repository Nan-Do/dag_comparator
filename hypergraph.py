from collections import namedtuple

# This will represent a node of the hypergraph
# next -> A dictionary representing the next level
# data -> The data for the node
Node = namedtuple('node', ['next', 'value'])


class Hypergraph:
    def __init__(self):
        self.root = dict()

    def __get_level_dictionary(self, nodes):
        current = self.root
        for node in nodes[:-1]:
            if node not in current:
                return None

            current = current[node].next
        return current

    def addValue(self, nodes, value):
        """
        Adds the value to the hypergraph following the sequence of nodes.

        Nodes must be a list of nodes that will be queried, if a node doesn't
        exist on the hypergraph it will be created, if it is not the last one
        on the sequence it will raise an error.
        The data for the nodes must be inmutable (set, strings, etc...)
        """

        d = self.__get_level_dictionary(nodes)
        if d is None:
            raise ValueError("Requested to add an invalid path on the " +
                             "hypergraph as one of it is itermediate" +
                             "nodes doesn't exist")

        new_node = Node(dict(), value)
        d[nodes[-1]] = new_node

    def getValue(self, nodes):
        """
        Returns the value associated with a node in the hypergraph.

        If the sequence of nodes doesn't exist it will return None.
        Nodes must be a list of nodes
        """

        d = self.__get_level_dictionary(nodes)

        if d is None or nodes[-1] not in d:
            return None

        return d[nodes[-1]].value
