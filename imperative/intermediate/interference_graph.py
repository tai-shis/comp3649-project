from networkx import Graph
from itertools import combinations

from intermediate.liveness import Liveness 

class InterferenceGraph:
    def __init__(self) -> None:
        self.interference_graph = Graph()

    def build_graph(self, liveness: Liveness, variables: set[str]) -> None:
        """
        Builds the interference graph based on the provided liveness analysis.

        :param liveness: The liveness analysis object.
        :type liveness: Liveness
        """

        # First, construct all nodes using the instruction buffer's variables
        for var in variables:
            self.interference_graph.add_node(var)

        # Then we add our edges
        for line in liveness.get_liveness():
            # Now check all combinations of live variables on this line
            combs = combinations([var for var, state in line.items() if state != 2], r=2)
            for var1, var2 in combs:
                self.interference_graph.add_edge(var1, var2)

    def __str__(self) -> str:
        return f"Interference Graph:\nNodes: {self.interference_graph.nodes()}\nEdges: {self.interference_graph.edges()}"