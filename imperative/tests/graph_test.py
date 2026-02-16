import io
import unittest
from input.scanner import Scanner
from input.parser import Parser
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph

class TestGraph(unittest.TestCase):

    def test_liveness(self):
        """
        Tests if the liveness class correctly generates liveness information for a simple set of instructions.
        """
        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        buffer = parser.parse()
        
        liveness = Liveness(buffer)
        liveness_data = liveness.get_liveness()

        self.assertEqual(len(liveness_data), 4)

        exit_block = liveness_data[-1]
        self.assertEqual(exit_block.get('a'), 1)
        self.assertEqual(exit_block.get('b'), 1)

    def test_build_graph(self):
        """
        Tests if the interference graph correctly extracts and adds all unique 
        variables as nodes to the graph.
        """

        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        buffer = parser.parse()
        
        liveness = Liveness(buffer)
        interferencegraph = InterferenceGraph()
        interferencegraph.build_graph(liveness, buffer.get_occured_variables())

        nodes = list(interferencegraph.interference_graph.nodes())
        
        self.assertIn('a', nodes)
        self.assertIn('b', nodes)
        self.assertIn('t1', nodes)
        self.assertEqual(len(nodes), 3)

    def test_coloring(self):
        """
        Tests if the graph coloring algorithm executes successfully and assigns colors 
        to all nodes without leaving any uncolored nodes.
        """

        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        buffer = parser.parse()
    
        liveness = Liveness(buffer)
        interferencegraph = InterferenceGraph()
        interferencegraph.build_graph(liveness, buffer.get_occured_variables())
        
        interferencegraph.color_graph(3)

        for node in interferencegraph.interference_graph.nodes():
            self.assertIsNotNone(interferencegraph.colors[node], f"Node {node} was not colored.")

    def test_edges(self):
        """
        Tests if the graph correctly draws edges between conflicting variables.
        """
        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        buffer = parser.parse()
        
        liveness = Liveness(buffer)
        interferencegraph = InterferenceGraph()
        interferencegraph.build_graph(liveness, buffer.get_occured_variables())

        # 'a' and 'b' are both live at the end, so they must interfere (have an edge)
        self.assertTrue(interferencegraph.interference_graph.has_edge('a', 'b'))

        # 'a' and 't1' are live at the same time, so they must interfere
        self.assertTrue(interferencegraph.interference_graph.has_edge('a', 't1'))

    def test_independent_variables(self):
        """
        Tests that variables that never overlap do NOT have an edge between them.
        """
        # 'x' is finished before 'y' ever starts
        input = "x = 1\nx = x + 1\ny = 2\nlive: y\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        buffer = parser.parse()
        
        liveness = Liveness(buffer)
        interferencegraph = InterferenceGraph()
        interferencegraph.build_graph(liveness, buffer.get_occured_variables())
        
        # There should be NO edge between x and y
        self.assertFalse(interferencegraph.interference_graph.has_edge('x', 'y'))

if __name__ == '__main__':
    unittest.main(verbosity=2)