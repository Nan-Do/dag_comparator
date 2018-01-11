import unittest

from hypergraph import Hypergraph


class TestHypergraph(unittest.TestCase):
    def test_addValueError(self):
        a = Hypergraph()
        nodes = [1, 2]

        self.assertRaises(ValueError,
                          a.addValue,
                          nodes,
                          0)

    def test_addValueSimple(self):
        a = Hypergraph()

        nodes = [1]
        a.addValue(nodes, 1)

    def test_addValue2(self):
        a = Hypergraph()

        nodes = [1]
        a.addValue(nodes, 1)

        nodes = [1, 2]
        a.addValue(nodes, 2)

    def test_getValueNonExisting(self):
        a = Hypergraph()

        nodes = [1, 2]
        res = a.getValue(nodes)

        self.assertEquals(res, None)

    def test_getValueExisting(self):
        a = Hypergraph()

        nodes = [1]
        a.addValue(nodes, 1)

        nodes = [1, 2]
        a.addValue(nodes, 2)
        
        res = a.getValue(nodes)
        self.assertEqual(res, 2)


if __name__ == '__main__':
    unittest.main()
