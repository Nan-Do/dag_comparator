import unittest

from collections import defaultdict

from directed_acyclic_graph import DirectedAcyclicGraphMapper


class testGenerateVariableCombinations(unittest.TestCase):
    # Function to initialize the data for the test suite
    def setUp(self):
        # First graph:
        #    ---a
        #   |  / \
        #   |  b-c
        #   |  | |
        #    --d e
        root = "a"
        graph = {
            "a": tuple("bcd"),
            "b": tuple("cd"),
            "c": tuple("e"),
            "d": tuple(""),
            "e": tuple("")
        }
        self.dag_mapper1 = DirectedAcyclicGraphMapper(root, graph)

        # Trivial example
        #       a
        #      / \
        #      b c
        root = "a"
        graph = {
            "a": tuple("bc"),
            "b": tuple(""),
            "c": tuple("")
        }
        self.dag_mapper2 = DirectedAcyclicGraphMapper(root, graph)

    # Tests to validate the input
    def test_SetVariableUnknownRoot(self):
        self.assertRaises(ValueError,
                          self.dag_mapper1.generateVariableCombinations,
                          "z",
                          2)

    def test_SetVariableIncorrectVariables(self):
        self.assertRaises(ValueError,
                          self.dag_mapper1.generateVariableCombinations,
                          "z",
                          0)

    # Tests to check that the solutions are correct
    def test_Set1VariableGraph1(self):
        valid_solution = set([('c',), ('d',), ('b',), ('e',)])
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 1)

        self.assertEqual(valid_solution, solution)

    def test_Set2VariablesGraph1(self):
        valid_solution = set([('d', 'e'), ('c',), ('b',), ('b', 'c'), ('e',),
                              ('d',), ('c', 'd'), ('b', 'e'), ('b', 'd')])
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 2)

        self.assertEqual(valid_solution, solution)

    def test_Set3VariablesGraph1(self):
        valid_solution = set([('d', 'e'), ('b', 'c', 'd'), ('c',), ('b',),
                              ('b', 'c'), ('e',), ('d',), ('b', 'd', 'e'),
                              ('c', 'd'), ('b', 'e'), ('b', 'd')])

        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 3)

        self.assertEqual(valid_solution, solution)

    def test_Set4VariableGraph1(self):
        # This should be the same as for 3 variables as you can put 4 variables
        # on the graph
        valid_solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                       3)
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 4)

        self.assertEqual(valid_solution, solution)

    # These tests check that we don't generate a solution that contains
    # more variables than the ones we specified on the parameter list
    def test_Set1VariableDoesntGenerate2orMoreVariablesGraph1(self):
        num_variables = 1
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)

    def test_Set2VariablesDoesntGenerate3orMoreVariablesGraph1(self):
        num_variables = 2
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)

    def test_Set3VariablesDoesntGenerate4orMoreVariablesGraph1(self):
        num_variables = 3
        solution = self.dag_mapper1.generateVariableCombinations(self.dag_mapper1.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)

    def test_Set1VariableGraph2(self):
        valid_solution = set([('b',), ('c',)])
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 1)

        self.assertEqual(valid_solution, solution)

    def test_Set2VariablesGraph2(self):
        valid_solution = set([('b',), ('c',), ('b', 'c')])
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 2)

        self.assertEqual(valid_solution, solution)

    def test_Set3VariableGraph2(self):
        valid_solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                       2)
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 3)

        self.assertEqual(valid_solution, solution)

    # These tests check that we don't generate a solution that contains
    # more variables than the ones we specified on the parameter list
    def test_Set1VariableDoesntGenerate2orMoreVariablesGraph2(self):
        num_variables = 1
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)

    def test_Set2VariablesDoesntGenerate3orMoreVariablesGraph2(self):
        num_variables = 2
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)

    def test_Set3VariablesDoesntGenerate4orMoreVariablesGraph2(self):
        num_variables = 3
        solution = self.dag_mapper2.generateVariableCombinations(self.dag_mapper2.root,
                                                                 num_variables)
        solution = all(map(lambda x: len(x) <= num_variables, solution))
        self.assertTrue(solution)


class testBuildSuccessors(unittest.TestCase):
    def setUp(self):
        # Trivial example
        #       a
        #      / \
        #      b c
        root = "a"
        graph = {
            "a": tuple("bc"),
            "b": tuple(""),
            "c": tuple("")
        }
        self.dag_mapper = DirectedAcyclicGraphMapper(root, graph)

    def test_successorsFromRootGraph2(self):
        solutions = {'a': {'c': 1, 'b': 1}}
        successors = defaultdict(dict)
        self.dag_mapper._DirectedAcyclicGraphMapper__buildSuccessors(self.dag_mapper.root,
                                                                     0,
                                                                     set(),
                                                                     successors)

        self.assertEqual(successors, solutions)

    def test_successorsFromLeafGraph2(self):
        solutions = {}
        successors = defaultdict(dict)
        self.dag_mapper._DirectedAcyclicGraphMapper__buildSuccessors('b',
                                                                     0,
                                                                     set(),
                                                                     successors)

        self.assertEqual(successors, solutions)


if __name__ == '__main__':
    unittest.main()
