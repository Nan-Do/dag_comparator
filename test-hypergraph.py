import unittest

from hypergraph import Hypergraph


class TestHypergraph(unittest.TestCase):
    def setUp(self):
        self.a = Hypergraph()

    def test_checkUnknownNode(self):
        self.assertRaises(ValueError,
                          self.a.updateNode,
                          "z",
                          2)

    def test_checkUnknownHyperedge(self):
        self.assertRaises(ValueError,
                          self.a.updateHyperedgeLabel,
                          ("z", "s"),
                          2)

    def test_addNode1(self):
        self.a.addNode('a', 1)

        self.assertEqual(self.a.getNodeValue('a'), 1)

    def test_addNode2(self):
        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        
        self.assertEqual(self.a.getNodeValue('a'), 1)
        self.assertEqual(self.a.getNodeValue('b'), 2)
 
    def test_addNode3(self):
        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        self.a.addNode('c', 3)
        
        self.assertEqual(self.a.getNodeValue('a'), 1)
        self.assertEqual(self.a.getNodeValue('b'), 2)
        self.assertEqual(self.a.getNodeValue('c'), 3)
        
    def test_updateNodeValue(self):
        self.a.addNode('a', 1)
        self.a.addNode('b', 2)

        self.a.updateNode('a', 3)

        self.assertEqual(self.a.getNodeValue('a'), 3)
        
    def test_addHyperedge1(self):
        he = ('a', 'b', 'c')

        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        self.a.addNode('c', 3)
        
        self.a.addHyperedge(he, "abc")

        self.assertEqual(self.a.getHyperedgeLabel(he), "abc")
 
    def test_addHyperedge2(self):
        he = ('a', 'b', 'c')
        he2 = ('d', 'b', 'c')

        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        self.a.addNode('c', 3)
        self.a.addNode('d', 4)
        
        self.a.addHyperedge(he, "abc")
        self.a.addHyperedge(he2, "dbc")

        self.assertEqual(self.a.getHyperedgeLabel(he2), "dbc")


    def test_updateHyperedgeLabel(self):
        he = ('a', 'b', 'c')
        he2 = ('d', 'b', 'c')

        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        self.a.addNode('c', 3)
        self.a.addNode('d', 4)
        
        self.a.addHyperedge(he, "abc")
        self.a.addHyperedge(he2, "dbc")

        self.a.updateHyperedgeLabel(he, "test")

        self.assertEqual(self.a.getHyperedgeLabel(he), "test")



    def test_checkHyperedgesAndNodes(self):
        he = ('a', 'b', 'c')
        he2 = ('d', 'b', 'c')
        solution = [he, he2]

        self.a.addNode('a', 1)
        self.a.addNode('b', 2)
        self.a.addNode('c', 3)
        self.a.addNode('d', 4)
        
        self.a.addHyperedge(he, "abc")
        self.a.addHyperedge(he2, "dbc")

        self.assertEqual(self.a.getHyperedgesFromNode('b'), solution)


 



if __name__ == '__main__':
    unittest.main()
