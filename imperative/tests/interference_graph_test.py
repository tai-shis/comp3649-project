import unittest
from io import StringIO
from unittest.mock import patch

from input.instruction import Instruction
from input.instruction_buffer import InstructionBuffer
from input.token import Token
from intermediate.interference_graph import InterferenceGraph
from intermediate.liveness import Liveness


def make_buffer(
    instructions: list[Instruction], live_objects: list[str]
) -> InstructionBuffer:
    """Helper to build an InstructionBuffer from instructions and live objects."""
    buf = InstructionBuffer()
    for instr in instructions:
        buf.add_instruction(instr)
    for live in live_objects:
        buf.add_live_object(live)
    return buf


def make_assignment(dest: str, operand: str, operand_type: int) -> Instruction:
    """Helper to create an assignment instruction."""
    return Instruction(2, Token(dest, 0), Token(operand, operand_type))


def make_graph_with_liveness(
    instructions: list[Instruction], live_objects: list[str], variables: set[str]
) -> InterferenceGraph:
    """Helper to build a complete InterferenceGraph from instructions, live objects, and variables."""
    buf = make_buffer(instructions, live_objects)
    liveness = Liveness(buf)
    graph = InterferenceGraph()
    graph.build_graph(liveness, variables)
    return graph


class TestInterferenceGraphConstruction(unittest.TestCase):
    def test_empty_graph_has_no_nodes(self):
        graph = InterferenceGraph()
        self.assertEqual(len(graph.interference_graph.nodes()), 0)

    def test_empty_graph_has_no_edges(self):
        graph = InterferenceGraph()
        self.assertEqual(len(graph.interference_graph.edges()), 0)

    def test_empty_graph_colors_empty(self):
        graph = InterferenceGraph()
        self.assertEqual(graph.colors, {})


class TestBuildGraph(unittest.TestCase):
    def test_nodes_added_for_all_variables(self):
        instr = make_assignment("x", "a", 1)
        graph = make_graph_with_liveness([instr], ["a"], {"x", "a", "b"})
        self.assertIn("a", graph.interference_graph.nodes())
        self.assertIn("b", graph.interference_graph.nodes())
        self.assertIn("x", graph.interference_graph.nodes())

    def test_all_colors_initialized_to_none(self):
        instr = make_assignment("x", "a", 1)
        graph = make_graph_with_liveness([instr], [], {"x", "a"})
        self.assertIsNone(graph.colors["x"])
        self.assertIsNone(graph.colors["a"])

    def test_edge_added_between_two_live_vars(self):
        # x = a + b, live: a, b — a and b are both live so should interfere
        instr = Instruction(
            0, Token("x", 0), Token("a", 1), Token("+", 3), Token("b", 1)
        )
        graph = make_graph_with_liveness([instr], ["a", "b"], {"x", "a", "b"})
        self.assertTrue(graph.interference_graph.has_edge("a", "b"))

    def test_no_edge_for_unlive_variable(self):
        # x = a, live: a — b is never live so no edge between a and b
        instr = make_assignment("x", "a", 1)
        graph = make_graph_with_liveness([instr], ["a"], {"x", "a", "b"})
        self.assertFalse(graph.interference_graph.has_edge("a", "b"))

    def test_no_edge_for_defined_variable(self):
        # x = a, live: a — x is defined (state 0) on the instruction line, not live
        instr = make_assignment("x", "a", 1)
        graph = make_graph_with_liveness([instr], ["a"], {"x", "a"})
        self.assertFalse(graph.interference_graph.has_edge("x", "a"))

    def test_no_self_edges(self):
        instr = make_assignment("x", "a", 1)
        graph = make_graph_with_liveness([instr], ["a"], {"x", "a"})
        for node in graph.interference_graph.nodes():
            self.assertFalse(graph.interference_graph.has_edge(node, node))

    def test_no_duplicate_edges(self):
        # Two instructions where a and b are both live — should still only have one edge
        instr1 = Instruction(
            0, Token("x", 0), Token("a", 1), Token("+", 3), Token("b", 1)
        )
        instr2 = Instruction(
            0, Token("y", 0), Token("a", 1), Token("+", 3), Token("b", 1)
        )
        graph = make_graph_with_liveness(
            [instr1, instr2], ["a", "b"], {"x", "y", "a", "b"}
        )
        # NetworkX graphs don't allow duplicate edges, so just verify the edge exists once
        self.assertEqual(graph.interference_graph.number_of_edges("a", "b"), 1)

class TestPossibleColors(unittest.TestCase):
    def test_all_colors_available_no_colored_neighbors(self):
        instr = Instruction(
            0, Token("x", 0), Token("a", 1), Token("+", 3), Token("b", 1)
        )
        graph = make_graph_with_liveness([instr], ["a", "b"], {"x", "a", "b"})
        # All neighbors of x are uncolored
        result = graph._possible_colors("x", 3)
        self.assertEqual(result, {0, 1, 2})

    def test_excludes_neighbor_colors(self):
        graph = InterferenceGraph()
        for var in ["x", "a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("x", "a")
        graph.interference_graph.add_edge("x", "b")
        graph.colors["a"] = 0
        graph.colors["b"] = 1
        result = graph._possible_colors("x", 3)
        self.assertEqual(result, {2})

    def test_no_colors_available(self):
        graph = InterferenceGraph()
        for var in ["x", "a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("x", "a")
        graph.interference_graph.add_edge("x", "b")
        graph.colors["a"] = 0
        graph.colors["b"] = 1
        result = graph._possible_colors("x", 2)
        self.assertEqual(result, set())

    def test_ignores_uncolored_neighbors(self):
        graph = InterferenceGraph()
        for var in ["x", "a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("x", "a")
        graph.interference_graph.add_edge("x", "b")
        graph.colors["a"] = 0
        # b is uncolored (None), should not be excluded
        result = graph._possible_colors("x", 2)
        self.assertEqual(result, {1})


class TestColorGraph(unittest.TestCase):
    def test_two_colorable_graph(self):
        instr = Instruction(
            0, Token("x", 0), Token("a", 1), Token("+", 3), Token("b", 1)
        )
        graph = make_graph_with_liveness([instr], ["a", "b"], {"x", "a", "b"})
        graph.color_graph(3)
        # Verify no two connected nodes share a color
        for u, v in graph.interference_graph.edges():
            self.assertNotEqual(graph.colors[u], graph.colors[v])

    def test_three_colorable_triangle(self):
        # a, b, c all interfere with each other — need 3 colors
        graph = InterferenceGraph()
        for var in ["a", "b", "c"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("a", "b")
        graph.interference_graph.add_edge("b", "c")
        graph.interference_graph.add_edge("a", "c")
        graph.color_graph(3)
        self.assertNotEqual(graph.colors["a"], graph.colors["b"])
        self.assertNotEqual(graph.colors["b"], graph.colors["c"])
        self.assertNotEqual(graph.colors["a"], graph.colors["c"])

    def test_insufficient_colors_raises_error(self):
        # Triangle needs 3 colors, only 2 provided
        graph = InterferenceGraph()
        for var in ["a", "b", "c"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("a", "b")
        graph.interference_graph.add_edge("b", "c")
        graph.interference_graph.add_edge("a", "c")
        with self.assertRaises(ValueError):
            graph.color_graph(2)

    def test_isolated_node_colored(self):
        graph = InterferenceGraph()
        graph.interference_graph.add_node("x")
        graph.colors["x"] = None
        graph.color_graph(1)
        self.assertEqual(graph.colors["x"], 0)


class TestPrintVariableInterferenceTable(unittest.TestCase):
    def test_correct_format(self):
        graph = InterferenceGraph()
        for var in ["a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("a", "b")
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_variable_interference_table()
            output = mock_out.getvalue()
        self.assertIn("a: b", output)
        self.assertIn("b: a", output)

    def test_isolated_node_empty_neighbors(self):
        graph = InterferenceGraph()
        graph.interference_graph.add_node("x")
        graph.colors["x"] = None
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_variable_interference_table()
            output = mock_out.getvalue()
        self.assertIn("x: ", output)

    def test_sorted_output(self):
        graph = InterferenceGraph()
        for var in ["c", "a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_variable_interference_table()
            output = mock_out.getvalue()
        lines = [
            l for l in output.strip().split("\n") if l and not l.startswith("Variable")
        ]
        node_names = [l.split(":")[0] for l in lines]
        self.assertEqual(node_names, sorted(node_names))


class TestPrintRegisterColouringTable(unittest.TestCase):
    def test_correct_format(self):
        graph = InterferenceGraph()
        graph.interference_graph.add_node("a")
        graph.colors["a"] = 0
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_register_colouring_table(1)
            output = mock_out.getvalue()
        self.assertIn("R0: a", output)

    def test_multiple_vars_per_register(self):
        graph = InterferenceGraph()
        for var in ["a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = 0
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_register_colouring_table(1)
            output = mock_out.getvalue()
        self.assertIn("R0: a, b", output)

    def test_empty_register(self):
        graph = InterferenceGraph()
        graph.interference_graph.add_node("a")
        graph.colors["a"] = 0
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            graph.print_register_colouring_table(2)
            output = mock_out.getvalue()
        self.assertIn("R1: ", output)


class TestStr(unittest.TestCase):
    def test_contains_nodes(self):
        graph = InterferenceGraph()
        for var in ["a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        output = str(graph)
        self.assertIn("Nodes:", output)

    def test_contains_edges(self):
        graph = InterferenceGraph()
        for var in ["a", "b"]:
            graph.interference_graph.add_node(var)
            graph.colors[var] = None
        graph.interference_graph.add_edge("a", "b")
        output = str(graph)
        self.assertIn("Edges:", output)

    def test_contains_colors(self):
        graph = InterferenceGraph()
        graph.interference_graph.add_node("a")
        graph.colors["a"] = 0
        output = str(graph)
        self.assertIn("Colors:", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
