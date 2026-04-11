from itertools import combinations

from intermediate.liveness import Liveness
from networkx import Graph


class InterferenceGraph:
    def __init__(self) -> None:
        self.interference_graph = Graph()
        self.colors: dict[str, int | None] = {}

    def build_graph(self, liveness: Liveness, variables: set[str]) -> None:
        """
        Builds interference graph based on liveness and instruction operands.
        Adds a node for every variable, then for every variable conflicting
        with another (i.e. live at the same time or appearing in the same
        instructions), an edge is added.
        
        :param liveness: The liveness object containing line-by-line 
        variable liveness states.
        :param variables: All variables occurring in the program.
        """
        for var in variables:
            self.interference_graph.add_node(var)
            self.colors[var] = None

        liveness_list = liveness.get_liveness()
        instructions = liveness.instruction_buffer.list_instructions()
        
        for i, line in enumerate(liveness_list[:-1]): 

            combs = combinations(
                [var for var, state in line.items() if state == 1], r=2
            )

            for var1, var2 in combs:
                if var1 in variables and var2 in variables:
                    # Ensure both are in colors dict (they should be, but guard anyway)
                    if var1 not in self.colors:
                        self.colors[var1] = None
                    if var2 not in self.colors:
                        self.colors[var2] = None
                    self.interference_graph.add_edge(var1, var2)

            # Also add edges between operands used on the same line
            # even if both are unlive — they must be in registers simultaneously
            instruction = instructions[i]
            operand_vars = [t.value for t in instruction.get_variables()[1:] if t.type != 2]
            operand_combs = combinations(operand_vars, r = 2)
            for var1, var2 in operand_combs:
                if var1 in variables and var2 in variables:
                    self.interference_graph.add_edge(var1, var2)

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
        nodes = list(self.interference_graph.nodes())

        # Base case: we've colored all nodes successfully
        if index >= len(nodes):
            return True

        node = nodes[index]

        # Skip if already colored (shouldn't normally happen, but safe guard)
        if self.colors[node] is not None:
            return self._solve_graph_coloring(index + 1, n)

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
            raise ValueError(
                "Failed to color the graph with the given number of colors."
            )

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
