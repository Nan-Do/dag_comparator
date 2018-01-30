from collections import namedtuple, defaultdict

TransitionData = namedtuple("TransitionData", ["continuation_nodes",
                                               "weight"])

TransitionState = namedtuple("TransitionState", ["continuation_node",
                                                 "accumulated_weight",
                                                 "transition_weight"])


class MappingsIterator:
    """
    Iterator class that enumerates the possibles paths of the hypergraph.

    Each path of the hypergraph is a possible mapping between the two graphs
    the hypergraph represents. As input parameters it takes a hypergraph and
    a source node to start computing the paths
    """
    # Kept for reference, probably slower than using sorted
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

    def __sort_best_transitions(self, best_transitions):
        """
        Auxiliary function used to sort transitions.

        It sorts the transitions decreasingly by the accumulated weight of the
        continuation nodes of the transition and its associated weight.
        """
        computed_weights = []
        for transition in best_transitions:
            value = sum(map(lambda x: x.accumulated_weight,
                            transition))
            # Each transition might have more than one continuation.
            # For each transition we only want to add the transition
            # weight only once
            value += transition[0].transition_weight
            computed_weights.append(value)

        sorting_list = zip(computed_weights, best_transitions)
        return map(lambda x: x[1], sorted(sorting_list, reverse=True))

    def __resetStates(self, hypergraph):
        """
        This functions builds the transitions dictionary for a given hypergraph.

        The transitions dictionary has as keys the firt element of a hyperedge
        and as values transition data elements. The transition data is formed
        by a list of continuation nodes, which are the rest of the nodes that
        form the hyperedge, and the weight associated with that hyperedge.
        Example
            Hyperedge ('aA', 'bB', 'cC') with a cost 0.5
            produces
            {'aA': TransitionData(ContinuationNodes=['bB', 'cC'],
                                  weight=0.5)}
        """
        transitions = defaultdict(list)
        for hyperedge in hypergraph.hyperedges:
            continuation_nodes = hyperedge[1:]
            weight = hypergraph.getHyperedgeLabel(hyperedge).weight

            transitions[hyperedge[0]].append(TransitionData(continuation_nodes,
                                                            weight))

        return transitions

    def __build_transitions_cache(self, hypergraph, node):
        """
        This function builds the cache for the transitions of a given hypergraph.

        The transitions cache is a dictionary in which as keys we have nodes of the
        hypergraph and as values lists of TransitionStates. The TransitionState
        contains the transition node (the node that used to continue the path on
        the hypergraph), its accumulated weight and the weight of the transition it
        belongs.
        Starting from the given node it goes to the leafes and in a bottom-up fashion
        computes the weights associated to each possible continuation node of the
        give node. The list of TransitionStates is sorted in a decreasing fashion.
        Later when we enumerate the solutions we will use the fact that the possible
        transitions are sorted to offer the best solution first.
        """
        if node in self.transitions_cache:
            for transition in self.transitions_cache[node]:
                yield transition

        if node not in self.node_transitions:
            st = TransitionState(None,
                                 hypergraph.getNodeWeight(node),
                                 0)
            # st = TransitionState(None, 0)
            self.transitions_cache[node] = [[st]]
            yield [st]
        else:
            sorted_transitions = []
            for transition in self.node_transitions[node]:
                transition_states = []
                hyperedge = (node,) + transition.continuation_nodes
                s = hypergraph.getHyperedgeLabel(hyperedge)
                for transition_node in transition.continuation_nodes:
                    n = self.__build_transitions_cache(hypergraph,
                                                       transition_node).next()
                    accumulated_weight = sum(map(lambda x: x.accumulated_weight,
                                                 n))
                    transition_states.append(TransitionState(transition_node,
                                                             accumulated_weight +\
                                                             n[0].transition_weight,
                                                             s.weight))
                sorted_transitions.append(transition_states)

            sorted_transitions = self.__sort_best_transitions(sorted_transitions)
            self.transitions_cache[node] = sorted_transitions
            for transition in sorted_transitions:
                yield transition

    # TODO: Currently it generates the best solution first and then
    # lexicografically the rest. Modify it to computed all the solutions in
    # order.
    def __enumerate_transitions(self, node):
        """
        This function enumerates the possible paths in a hypergraph given a
        node.

        Using the previously computed transitions cache this function uses
        bactracking and generators to enumerate the possible transitions of
        the hypergraph.
        """
        for transition in self.transitions_cache[node]:
            solution = [transition]
            continuations = []
            continuation_nodes = []

            for continuation in transition:
                c = continuation.continuation_node
                # If the continuation node is none we reached the base case
                # upload the solution and finish the generator
                if c is None:
                    yield solution
                    return
                # First batch of generators
                continuations.append(self.__enumerate_transitions(c))
                # Used to refresh the generators when they are consumed
                continuation_nodes.append(c)

            counter = 0
            while True:
                c = next(continuations[counter], None)

                # We reached the end of the generator
                if c is None:
                    # Not the first generator, refresh it and update the
                    # solution.
                    if counter != 0:
                        # Update the solutions to the current transition
                        solution = [transition]
                        # Refresh the current generator
                        g = self.__enumerate_transitions(continuation_nodes[counter])
                        continuations[counter] = g
                        # Update the counter
                        counter -= 1
                        continue

                    break

                solution.extend(c)
                counter += 1
                # End of the generators list
                if counter == len(continuations):
                    yield solution
                    # Remove the elements added by c
                    solution = solution[:-len(c)]
                    # Update the counter
                    counter -= 1

    def __init__(self, hypergraph, initial_node):
        self.node_transitions = self.__resetStates(hypergraph)
        self.transitions_cache = dict()

        if initial_node not in self.node_transitions:
            raise ValueError("The specified initial node doesn't start a hyperedge")

        self.__build_transitions_cache(hypergraph, initial_node).next()
        self.generator = self.__enumerate_transitions(initial_node)

    def __iter__(self):
        return self

    def next(self):
        return self.generator.next()
