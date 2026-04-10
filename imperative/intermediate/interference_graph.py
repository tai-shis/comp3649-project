from networkx import Graph
from itertools import combinations

from intermediate.liveness import Liveness 

class InterferenceGraph:
    def __init__(self) -> None:
        self.interference_graph = Graph()
        self.colors: dict[str, int | None] = {}

    def build_graph(self, liveness: Liveness, variables: set[str]) -> None:
        """
        Builds the interference graph based on the provided liveness analysis.

        :param liveness: The liveness analysis object.
        :type liveness: Liveness
        :param variables: The set of all variable names to add as nodes.
        :type variables: set[str]
        """

        # First, construct all nodes using the instruction buffer's variables
        for var in variables:
            self.interference_graph.add_node(var)
            self.colors[var] = None

        # Then we add our edges
        for line in liveness.get_liveness():
            # Now check all combinations of live variables on this line
            combs = combinations([var for var, state in line.items() if state != 2], r=2)
            for var1, var2 in combs:
                self.interference_graph.add_edge(var1, var2)

    def _is_solved(self) -> bool:
        """
        Checks if the interference graph has been successfully colored.

        :return: True if the graph is properly coloured, false otherwise
        :rtype: bool
        """

        for node in self.interference_graph.nodes():
            color = self.colors[node]

            if color is None:
                return False
        
            # Make sure no neighbors have the same color
            for neighbor in self.interference_graph.neighbors(node):
                if color == self.colors[neighbor]:
                    return False
            
        return True

    def _possible_colors(self, node: str, n: int) -> set[int]:
        """
        Returns a set of possible colors for a given node.

        :param node: The node to check.
        :type node: str
        :param n: The number of colors available.
        :type n: int
        :return: A set of possible colors for the node.
        :rtype: set[int]
        """
        used = set()
        for neighbor in self.interference_graph.neighbors(node):
            if self.colors[neighbor] is not None:
                used.add(self.colors[neighbor])

        return set(range(n)) - used

    def _solve_graph_coloring(self, index: int, n: int) -> bool:
        """
        Recursively attempts to color the graph using backtracking.

        :param index: Index of the current node to color.
        :type index: int
        :param n: Number of colors available.
        :type n: int
        :return: True if a valid coloring was found, False otherwise.
        :rtype: bool
        """
        if self._is_solved():
            return True
        
        node = list(self.interference_graph.nodes())[index]
        for color in self._possible_colors(node, n):
            self.colors[node] = color

            if self._solve_graph_coloring(index + 1, n):
                return True
            
            self.colors[node] = None

        return False


    def color_graph(self, n: int) -> None:
        """
        Colors the interference graph using a greedy coloring algorithm.

        :param n: The number of colors to use.
        :type n: int
        """
        if self._solve_graph_coloring(0, n):
            print("Graph successfully colored.")
        else:
            raise ValueError("Failed to color the graph with the given number of colors.")        
    
    def print_variable_interference_table(self) -> None:
        """
        Prints the variable interference table.
        """
        print("Variable Interference Table:")

        # sorting to make sure variables print in the same order
        for var in sorted(self.interference_graph.nodes()):
            neighbors = list(self.interference_graph.neighbors(var))
            neighbors.sort()
            
            output = ", ".join(neighbors)
            print(f"{var}: {output}")
            
        print()

    def print_register_colouring_table(self, n: int) -> None:
        """
        Prints the register colouring table.

        :param n: The number of registers used.
        :type n: int
        """
        print("Register Colouring Table:")
        
        for i in range(n):
            # get all variables assigned to the register
            assigned_vars = []
            for var, color in self.colors.items():
                if color == i:
                    assigned_vars.append(var)
            
            assigned_vars.sort()
            
            output = ", ".join(assigned_vars)
            print(f"R{i}: {output}")
            
        print()

    def __str__(self) -> str:
        string = f"Interference Graph:\n\
                    Nodes: {self.interference_graph.nodes()}\n\
                    Edges: {self.interference_graph.edges()}\n\
                    Colors: {self.colors}"

        return string