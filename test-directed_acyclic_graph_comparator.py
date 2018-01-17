import unittest

from datastructures import DirectedAcyclicGraph

from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator


class testBuildHypergraph(unittest.TestCase):
    def setUp(self):
        root = "a"
        links = {
            "a": tuple("bc"),
            "b": tuple("d"),
            "c": tuple("e"),
            "d": tuple(""),
            "e": tuple("")
        }
        dag1 = DirectedAcyclicGraph(root, links)

        root = "A"
        links = {
            "A": tuple("BC"),
            "B": tuple(),
            "C": tuple("D"),
            "D": tuple()
        }
        dag2 = DirectedAcyclicGraph(root, links)

        self.comparator = DirectedAcyclicGraphComparator(dag1, dag2)
        self.comparator.buildHyperGraph()

    def test_numberOfNodes(self):
        number = 20

        self.assertEqual(number,
                         len(self.comparator.hypergraph.nodes))

    def test_numberOfHyperedges(self):
        number = 30

        self.assertEqual(number,
                         len(self.comparator.hypergraph.hyperedges))

    def test_aANodeScore(self):
        node = ('a', 'A')
        score = 3.74

        self.assertAlmostEqual(score,
                               self.comparator.hypergraph.getNodeValue(node))

    def test_bBNodeScore(self):
        node = ('b', 'B')
        score = 1.0

        self.assertAlmostEqual(score,
                               self.comparator.hypergraph.getNodeValue(node))

    def test_dDNodeScore(self):
        node = ('d', 'D')
        score = 1.0

        self.assertAlmostEqual(score,
                               self.comparator.hypergraph.getNodeValue(node))

    def test_aCNodeScore(self):
        node = ('a', 'C')
        score = 1.368

        self.assertAlmostEqual(score,
                               self.comparator.hypergraph.getNodeValue(node))

    def test_cCNodeScore(self):
        node = ('c', 'C')
        score = 1.94

        self.assertAlmostEqual(score,
                               self.comparator.hypergraph.getNodeValue(node))

    def test_hyperedge1(self):
        hyperedge = (('a', 'A'), ('b', 'B'), ('e', 'C'))

        self.assertEquals(self.comparator.hypergraph.containsHyperedge(hyperedge),
                          True)

    def test_hyperedge2(self):
        hyperedge = (('c', 'A'), ('e', 'B'))

        self.assertEquals(self.comparator.hypergraph.containsHyperedge(hyperedge),
                          True)

    def test_hyperedge3(self):
        hyperedge = (('b', 'C'), ('d', 'D'))

        self.assertEquals(self.comparator.hypergraph.containsHyperedge(hyperedge),
                          True)

    def test_hyperedge4(self):
        hyperedge = (('b', 'C'), ('e', 'E'))

        self.assertEquals(self.comparator.hypergraph.containsHyperedge(hyperedge),
                          False)

    def test_hyperedge5(self):
        hyperedge = (('d', 'C'), ('e', 'E'))

        self.assertEquals(self.comparator.hypergraph.containsHyperedge(hyperedge),
                          False)

if __name__ == '__main__':
    unittest.main()
