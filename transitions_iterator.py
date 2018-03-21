from collections import defaultdict, namedtuple
from copy import deepcopy

# This data type will contain the information to represent the
# hyperedges of the hypergraph as transitions. Check the
# function __resetStates for more information.
HyperedgeTransition = namedtuple("HyperedgeTransition", ["continuation_nodes"])


# This data type represents a continuation, that is given a path
# which is the next node that we can take. This node has an associated
# value in the path. The node is represented by the continuation_node
# which will be a node of the hypergraph and the accumulated_weight
# will represent the associated cost in the path.
# Continuation = namedtuple("Continuation", ["continuation_node",
#                                            "accumulated_weight"])
class Continuation:
    def __init__(self, continuation_node, accumulated_weight):
        self.continuation_node = continuation_node
        self.accumulated_weight = accumulated_weight

    # Pretty printing
    def __repr__(self):
        return "Continuation(continuation_node=" + str(self.continuation_node) +\
                ", accumluated_weight=" + str(self.accumulated_weight) + ")"

    # Required to pass the tests
    def __eq__(self, other, error=0.0001):
        return self.continuation_node == other.continuation_node and\
                abs(self.accumulated_weight - other.accumulated_weight) < error

    # Required for compatibilty with the named tuple
    def __getitem__(self, index):
        if index < 0:
            index = 2 - index
        if index < 0 or index > 1:
            raise IndexError("index out of range")

        if index == 0:
            return self.continuation_node
        else:
            return self.accumulated_weight

# This data type represents a Tranisition. A transition means all the
# possible paths that we can't take given a node. The transisition has an
# associated cost.
# The continuations represent all the possible paths we can take The
# continuations will be a list of lists of Continuation
# The weight  is the associated weight with the transition.
Transition = namedtuple("Transition", ["continuations",
                                       "weight"])


class TransitionsIterator:
    """
    Iterator class that enumerates the possibles paths of the hypergraph.

    Each path of the hypergraph is a possible mapping between the two graphs
    the hypergraph represents. As input parameters it takes a hypergraph and
    a source node to start computing the paths
    """
    # Kept for reference, probably slower than using sorted (Deprecated)
    def __insert_transition_sorted_by_weight(self, l, state):
        """
        Auxiliary function used to sort transitions (Deprecated).
        """
        weight = state.weight
        lo = insert_position = 0
        hi = len(l)
        while lo < hi:
            mid = (lo + hi) / 2
            weight1 = l[mid-1].weight
            weight2 = l[mid].weight

            if weight1 >= weight >= weight2:
                insert_position = mid
                break

            if weight2 < weight:
                hi = mid - 1
            else:
                lo = mid + 1
                insert_position = lo

        l.insert(insert_position,
                 state)

    def __sort_transitions(self, transitions):
        """
        Auxiliary function used to sort continuations.

        It sorts the continuations decreasingly by the accumulated weight of
        the continuation nodes of the transition and its associated weight.
        It uses the auxiliary function compute_weight to obtain the weight
        of a transition. The weight of a transition is the sum of the 
        accumulated weight of the continuation nodes and the weight associated
        with the transition itself.
        """
        def compute_weight(transition):
            value = sum(map(lambda x: x.accumulated_weight,
                            transition.continuations))
            value += transition.weight
            return value

        return transitions.sort(key=compute_weight, reverse=True)

    def __resetStates(self, hypergraph):
        """
        This functions builds the transitions dictionary for a given hypergraph.

        The transitions dictionary has as keys the firt element of a hyperedge
        and as values the rest of the elements.
        Example:
            Hyperedge ('aA', 'bB', 'cC')
            produces
            { 'aA': HyperedgeTransition(['bB', 'cC']) }
        """
        hyperege_transitions = defaultdict(list)
        for hyperedge in hypergraph.hyperedges:
            continuation_nodes = hyperedge[1:]
            hyper_trans = HyperedgeTransition(continuation_nodes)
            hyperege_transitions[hyperedge[0]].append(hyper_trans)

        return hyperege_transitions

    def __build_transitions_cache(self, hypergraph, node):
        """
        This function builds the cache of transitions for a given hypergraph
        and node.

        The transitions cache is a dictionary in which as keys we have nodes of
        the hypergraph and as values TransitionStates. The TransitionState
        contains a list of continuations and its associated weight. The
        continuations is a list of continuations. Each continuation contains
        a continuation_node wich indicates the next step on the path and its
        accumulated weight.
        Starting from the given node it goes to the leafes and in a bottom-up
        fashion computes the weights associated to each possible continuation
        node of the give node. The list of TransitionStates is sorted in a
        decreasing fashion. Later when we enumerate the solutions we will use
        the fact that the possible transitions are sorted to offer the best
        solution first.
        """
        if node in self.transitions_cache:
            yield self.transitions_cache[node]

        if node not in self.hyperege_transitions:
            c = Continuation(None,
                             hypergraph.getNodeWeight(node))
            t = Transition((c,), 0)
            self.transitions_cache[node] = [t]
            yield [t]
        else:
            # Add the option to compare whole subgraphs without variables
            # If transitions is an empty list whole subgraphs will not be
            # compared
            # transitions = []
            c = Continuation(None,
                             hypergraph.getNodeWeight(node))
            transitions = [Transition((c,), 0)]
            for hyperedge_transition in self.hyperege_transitions[node]:
                transition = []
                for continuation_node in hyperedge_transition.continuation_nodes:
                    n = self.__build_transitions_cache(hypergraph,
                                                       continuation_node).next()
                    accumulated_weight = sum(map(lambda x: x.accumulated_weight,
                                                 n[0].continuations))
                    accumulated_weight += n[0].weight
                    c = Continuation(continuation_node, accumulated_weight)
                    transition.append(c)

                hyperedge = (node,) + tuple(map(lambda x: x.continuation_node,
                                                transition))
                t = Transition(transition,
                               hypergraph.getHyperedgeLabel(hyperedge).weight)
                transitions.append(t)

            self.__sort_transitions(transitions)
            self.transitions_cache[node] = transitions
            yield transitions

    # TODO: Currently it generates the best solution first and then
    # lexicografically the rest. Modify it to computed all the solutions in
    # order.
    def __enumerate_transitions(self, node):
        """
        This function enumerates the possible paths in a hypergraph given a
        node.

        Using the previously computed transitions cache this function uses
        bactracking and generators to enumerate the possible transitions of
        the hypergraph. It generates the best solution first and then the
        rest in an topological sort.
        """
        # Extract the current transition
        for transition in self.transitions_cache[node]:
            solution = ((transition.continuations, transition.weight),)
            # Build the generators
            generators = []
            generator_backups = []

            for c in transition.continuations:
                c = c.continuation_node
                # Reached the base case, yield the solution and finish the
                # generator
                if c is None:
                    yield solution
                    return
                generators.append(self.__enumerate_transitions(c))
                # Used to refresh the generators when they are consumed
                generator_backups.append(c)

            counter = 0
            while True:
                c = next(generators[counter], None)

                # Reached the end of the generator
                if c is None:
                    if counter == 0:
                        break

                    # Update the solution
                    solution = ((transition.continuations, transition.weight),)
                    # Refresh the current generator
                    g = self.__enumerate_transitions(generator_backups[counter])
                    generators[counter] = g
                    # Update the counter
                    counter -= 1

                    continue

                # Update the accumulated_weight
                # The commented out lines are in case the usage of the
                # the named tuple instead the class is preferred.
                # continuation_node = solution[0][0][counter].continuation_node
                total_weight = sum(map(lambda x: x.accumulated_weight,
                                       c[0][0])) + c[0][1]
                # solution[0][0][counter] = Continuation(continuation_node,
                #                                        total_weight)
                solution[0][0][counter].accumulated_weight = total_weight
                counter += 1
                solution += c
                # Reached the end of the generators list
                if counter == len(generators):
                    yield solution
                    # Remove the elements added by c
                    solution = solution[:-len(c)]
                    # Update the counter
                    counter -= 1

    def __init__(self, hypergraph, initial_node):
        self.hyperege_transitions = self.__resetStates(hypergraph)
        self.transitions_cache = dict()

        if initial_node not in self.hyperege_transitions:
            raise ValueError("The specified initial node doesn't start a "
                             "hyperedge")

        self.__build_transitions_cache(hypergraph, initial_node).next()
        self.generator = self.__enumerate_transitions(initial_node)

    def __iter__(self):
        return self

    def next(self, deep_copy=True):
        a = self.generator.next()

        if not deep_copy:
            return a
        else:
            return deepcopy(a)

