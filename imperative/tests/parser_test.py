import io
import unittest
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer

class TestParser(unittest.TestCase):

    def test_basic_assignment(self):
        """
        Tests the parser to ensure it can handle a basic assignment like 'a = 1'
        """
        input = "a = 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)

        buffer = parser.parse()
        instructions = buffer.list_instructions()

        self.assertEqual(len(instructions), 1)
        self.assertEqual(instructions[0], "a = 1")

    def test_arithmetic_operation(self):
        """
        Tests the parser to ensure it can handle an arithmetic operation like 'a = b + c'.
        """
        input = "a = b + c\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)


        buffer = parser.parse()
        instructions = buffer.list_instructions()

        self.assertEqual(len(instructions), 1)
        self.assertEqual(instructions[0], "a = b + c")

    def test_unary_operation(self):
        """
        Tests the parser to ensure it can handle a basic assignment like 'a = -b\n'
        """
        input = "a = -b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)

        buffer = parser.parse()
        instructions = buffer.list_instructions()

        self.assertEqual(len(instructions), 1)
        self.assertEqual(instructions[0], "a = -b")

    def test_missing_operands(self):
        """
        Tests the parser to ensure it can handle missing operands like 'a = +\n'
        """
        input = "a = +\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)

        with self.assertRaises(ValueError):
            parser.parse()

    def test_multiple_lines(self):
        """
        Tests parsing multiple lines to ensure the buffer is 
        collecting them in the correct order.
        """
        input = "a = 1\nb = a + 2\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)

        buffer = parser.parse()
        instructions = buffer.list_instructions()

        self.assertEqual(len(instructions), 2)
        self.assertEqual(instructions[0], "a = 1")
        self.assertEqual(instructions[1], "b = a + 2")

    def test_live_object(self):
        """
        Tests if the parser identifies live objects correctly.
        """
        input = "a = 1\nlive: a"
        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)

        buffer = parser.parse()
        live_objects = buffer.list_live_objects()

        self.assertEqual(len(live_objects), 1)
        self.assertEqual(live_objects[0], "a")

if __name__ == '__main__':
    unittest.main(verbosity=2)