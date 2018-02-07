import unittest

from datastructures import DirectedAcyclicGraph
from directed_acyclic_graph_comparator import DirectedAcyclicGraphComparator
from mappings_iterator import MappingsIterator, Continuation


class mappingsBigGraphTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(mappingsBigGraphTestCase, cls).setUpClass()
        root = "a"
        links = {
            "a": tuple("bcd"),
            "b": tuple("ej"),
            "c": tuple("f"),
            "d": tuple("hi"),
            "e": tuple("qgs"),
            "f": tuple("z"),
            "g": tuple(""),
            "h": tuple("rtu"),
            "i": tuple("wx"),
            "j": tuple("kl"),
            "k": tuple("mn"),
            "l": tuple("y"),
            "m": tuple(""),
            "n": tuple(""),
            "o": tuple(""),
            "p": tuple(""),
            "q": tuple(""),
            "r": tuple(""),
            "s": tuple(""),
            "t": tuple("vop"),
            "u": tuple(""),
            "v": tuple(""),
            "w": tuple(""),
            "x": tuple(""),
            "y": tuple(""),
            "z": tuple("")
        }
        dag1 = DirectedAcyclicGraph(root, links)

        root = "A"
        links = {
            "A": tuple("BD"),
            "B": tuple("CEF"),
            "C": tuple("KGL"),
            "D": tuple("HIJ"),
            "E": tuple("MN"),
            "F": tuple("Z"),
            "G": tuple(""),
            "H": tuple("RTU"),
            "I": tuple("WX"),
            "J": tuple("YOQ"),
            "K": tuple("PSV"),
            "L": tuple(""),
            "M": tuple(""),
            "N": tuple(""),
            "O": tuple(""),
            "P": tuple(""),
            "Q": tuple(""),
            "R": tuple(""),
            "S": tuple(""),
            "T": tuple(""),
            "U": tuple(""),
            "V": tuple(""),
            "W": tuple(""),
            "X": tuple(""),
            "Y": tuple(""),
            "Z": tuple("")
        }
        dag2 = DirectedAcyclicGraph(root, links)
        comparator = DirectedAcyclicGraphComparator(dag1, dag2)
        comparator.buildHyperGraph()

        it = MappingsIterator(comparator.hypergraph,
                              ('a', 'A'))

        cls.best = it.next()
        cls.it = it

    def test_BestScore(self):
        res = sum(map(lambda x: x.accumulated_weight,
                  self.best[0][0])) + self.best[0][1]

        self.assertAlmostEqual(res,
                               6.97021978022)

    def test_firstSolution(self):
        res = ([Continuation(continuation_node=('b', 'B'), accumulated_weight=3.09021978021978), Continuation(continuation_node=('d', 'D'), accumulated_weight=2.88)], 1.0)

        self.assertEqual(res,
                         self.best[0])

    def test_firstSolution2(self):
        res = ([Continuation(continuation_node=('j', 'C'), accumulated_weight=2.327142857142857)], 0.7630769230769231)
        self.assertEqual(res,
                         self.best[1])

    def test_firstSolution3(self):
        res = ([Continuation(continuation_node=('k', 'K'), accumulated_weight=1.5899999999999999)], 0.7371428571428571)

        self.assertEqual(res,
                         self.best[2])

    def test_firstSolutionLength(self):
        res = len(self.best)

        self.assertEqual(res, 8)

    def test_IterateOver10000Mappings(self):
        for _ in xrange(10000):
            self.it.next(False)

        self.assertTrue(True)

    def test_NextScoreIsWorseThanTheBest(self):
        n = self.it.next()
        max_score = sum(map(lambda x: x.accumulated_weight,
                            self.best[0][0])) + self.best[0][1]
        res = sum(map(lambda x: x.accumulated_weight,
                  n[0][0])) + n[0][1]

        self.assertGreater(max_score, res)

    def test_NextNextScoreIsWorseThanTheBest(self):
        n = self.it.next()
        max_score = sum(map(lambda x: x.accumulated_weight,
                            self.best[0][0])) + self.best[0][1]
        res = sum(map(lambda x: x.accumulated_weight,
                  n[0][0])) + n[0][1]

        self.assertGreater(max_score, res)


class mappingsSmallGraphTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(mappingsSmallGraphTestCase, cls).setUpClass()
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
            "B": tuple("D"),
            "C": tuple(),
            "D": tuple()
        }
        dag2 = DirectedAcyclicGraph(root, links)

        comparator = DirectedAcyclicGraphComparator(dag1, dag2)
        comparator.buildHyperGraph()

        it = MappingsIterator(comparator.hypergraph,
                              ('a', 'A'))

        cls.derivations = []
        for pos, x in enumerate(it):
            cls.derivations.append(x)
        cls.number = pos

    def test_ThereMustBe17Derivations(self):
        self.assertEqual(self.number, 17)

    def testBestScore(self):
        best = self.derivations[0]
        res = sum(map(lambda x: x.accumulated_weight,
                  best[0][0])) + best[0][1]
        self.assertAlmostEqual(res,
                               3.8)

    def testBestScoreIsGreaterThanLastOne(self):
        best = self.derivations[0]
        last = self.derivations[-1]
        max = sum(map(lambda x: x.accumulated_weight,
                  best[0][0])) + best[0][1]
        last = sum(map(lambda x: x.accumulated_weight,
                   last[0][0])) + last[0][1]
        self.assertGreater(max, last)

if __name__ == '__main__':
    unittest.main()
