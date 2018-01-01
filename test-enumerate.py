import unittest

from enumerate import generateVariableCombinations


class testGenerateVariableCombinations(unittest.TestCase):
    # Function to initialize the data for the test suite
    def setUp(self):
        # First graph:
        #    ---a
        #   |  / \
        #   |  b-c
        #   |  | |
        #    --d e
        self.root_1 = "a"
        self.graph_1 = {
            "a": tuple("bcd"),
            "b": tuple("cd"),
            "c": tuple("e"),
            "d": tuple(""),
            "e": tuple("")
        }

        # Trivial example
        self.root_2 = "a"
        self.graph_2 = {
            "a": tuple("bc"),
            "b": tuple(""),
            "c": tuple("")
        }

    # Tests to validate the input
    def test_SetVariableEmtpyGraph(self):
        self.assertRaises(ValueError,
                          generateVariableCombinations,
                          self.root_1,
                          dict(),
                          2)

    def test_SetVariableUnknownRoot(self):
        self.assertRaises(ValueError,
                          generateVariableCombinations,
                          "z",
                          self.graph_1,
                          2)

    def test_SetVariableIncorrectVariables(self):
        self.assertRaises(ValueError,
                          generateVariableCombinations,
                          "z",
                          self.graph_1,
                          0)

    # Tests to check that the solutions are correct
    def test_Set1VariableGraph1(self):
        valid_solution = set([('c',), ('d',), ('b',), ('e',)])
        solution = generateVariableCombinations(self.root_1, self.graph_1, 1)

        self.assertSetEqual(valid_solution, solution)

    def test_Set2VariablesGraph1(self):
        valid_solution = set([('d', 'e'), ('c',), ('b',), ('b', 'c'), ('e',),
                              ('d',), ('c', 'd'), ('b', 'e'), ('b', 'd')])
        solution = generateVariableCombinations(self.root_1, self.graph_1, 2)

        self.assertSetEqual(valid_solution, solution)

    def test_Set3VariablesGraph1(self):
        valid_solution = set([('d', 'e'), ('b', 'c', 'd'), ('c',), ('b',),
                              ('b', 'c'), ('e',), ('d',), ('b', 'd', 'e'),
                              ('c', 'd'), ('b', 'e'), ('b', 'd')])

        solution = generateVariableCombinations(self.root_1, self.graph_1, 3)

        self.assertSetEqual(valid_solution, solution)

    def test_Set4VariableGraph1(self):
        # This should be the same as for 3 variables as you can put 4 variables
        # on the graph
        valid_solution = generateVariableCombinations(self.root_1,
                                                      self.graph_1,
                                                      3)
        solution = generateVariableCombinations(self.root_1, self.graph_1, 4)

        self.assertSetEqual(valid_solution, solution)

    def test_Set1VariableGraph2(self):
        valid_solution = set([('b',), ('c',)])
        solution = generateVariableCombinations(self.root_2, self.graph_2, 1)

        self.assertSetEqual(valid_solution, solution)

    def test_Set2VariableGraph2(self):
        valid_solution = set([('b',), ('c',), ('b', 'c')])
        solution = generateVariableCombinations(self.root_2, self.graph_2, 2)

        self.assertSetEqual(valid_solution, solution)

    def test_Set3VariableGraph2(self):
        valid_solution = generateVariableCombinations(self.root_2,
                                                      self.graph_2,
                                                      2)
        solution = generateVariableCombinations(self.root_2, self.graph_2, 3)

        self.assertSetEqual(valid_solution, solution)

if __name__ == '__main__':
    unittest.main()
