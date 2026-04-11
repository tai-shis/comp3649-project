import io
import unittest
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from input.token import Token

def create_parser_from_string(input_string: str) -> Parser:
    scanner = Scanner(io.StringIO(input_string))
    return Parser(scanner)

class TestValidateInstruction(unittest.TestCase):
    def test_valid_binary(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("a", 1),
            Token("+", 3),
            Token("b", 1),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, 0)

    def test_valid_binary_with_literal(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("1", 2),
            Token("+", 3),
            Token("2", 2),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, 0)

    def test_unary_operator(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("-", 3),
            Token("a", 1),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, 1)

    def test_assignment(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("a", 1),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, 2)

    def test_valid_assignment_with_literal(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("29", 2),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, 2)

    def test_invalid_length(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, -1)
    
    def test_wrong_token_order(self):
        instruction = [
            Token("=", 4),
            Token("x", 0),
            Token("a", 1),
            Token("+", 3),
            Token("b", 1),
            Token("\n", 7)
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, -1) 

    def test_missing_newline(self):
        instruction = [
            Token("x", 0),
            Token("=", 4),
            Token("a", 1),
            Token("+", 3),
            Token("b", 1),
        ]
        parser = create_parser_from_string("")
        ins_type = parser._validate_instruction(instruction)
        self.assertEqual(ins_type, -1) 

class TestParseInstructions(unittest.TestCase):
    def test_single_binary(self):
        parser = create_parser_from_string("x = a + b\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        occurred_vars = parser.occurred_variables
        instructions = buffer.list_instructions()
        self.assertEqual(occurred_vars, {"x", "a", "b"})
        self.assertEqual(str(instructions[0]), "x = a + b")

    def test_single_unary(self):
        parser = create_parser_from_string("x = - a\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        occurred_vars = parser.occurred_variables
        instructions = buffer.list_instructions()
        self.assertEqual(occurred_vars, {"x", "a"})
        self.assertEqual(str(instructions[0]), "x = -a")

    def test_single_assignment(self):
        parser = create_parser_from_string("x = 32\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        occurred_vars = parser.occurred_variables
        instructions = buffer.list_instructions()
        self.assertEqual(occurred_vars, {"x"})
        self.assertEqual(str(instructions[0]), "x = 32")

    def test_multiple_instructions(self):
        parser = create_parser_from_string("x = a + b\ny = x\nz = y\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        occurred_vars = parser.occurred_variables
        instructions = buffer.list_instructions()
        self.assertEqual(occurred_vars, {"x", "a", "b", "y", "z"})
        self.assertEqual(str(instructions[0]), "x = a + b")
        self.assertEqual(str(instructions[1]), "y = x")
        self.assertEqual(str(instructions[2]), "z = y")

    def test_stops_at_live(self):
        parser = create_parser_from_string("x = a + b\nlive:\na,")
        buffer = InstructionBuffer()
        parse_result = parser._parse_instructions(buffer)
        occurred_vars = parser.occurred_variables
        instructions = buffer.list_instructions()
        self.assertEqual(parse_result, False)
        self.assertEqual(occurred_vars, {"x", "a", "b"})
        self.assertEqual(str(instructions[0]), "x = a + b")
        self.assertEqual(len(instructions), 1)

    def test_return_true_on_EOF(self):
        parser = create_parser_from_string("")
        isEOF = parser._parse_instructions(Token("", -1))
        self.assertEqual(isEOF, True)

    def test_raise_err_on_invalid_ins(self):
        parser = create_parser_from_string("= x a +\n")
        buffer = InstructionBuffer()
        with self.assertRaises(ValueError):
            parser._parse_instructions(buffer)

class TestParseLive(unittest.TestCase):
    def test_live_no_vars(self):
        parser = create_parser_from_string("x = a\nlive:\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        parser._parse_live(buffer)
        live_objs = buffer.list_live_objects()
        self.assertEqual(live_objs, [])

    def test_valid_obj(self):
        parser = create_parser_from_string("x = a\nlive:\na,")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        parser._parse_live(buffer)
        live_objs = buffer.list_live_objects()
        self.assertEqual(live_objs, ["a"])
    
    def test_multiple_valid_objs(self):
        parser = create_parser_from_string("x = a + b\nb = c + 1\nlive:\na, b, c,")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        parser._parse_live(buffer)
        live_objs = buffer.list_live_objects()
        self.assertEqual(live_objs, ["a", "b", "c"])
    
    def test_duplicate_objs_dropped(self):
        parser = create_parser_from_string("x = a + b\nlive:\na, a, b,")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        parser._parse_live(buffer)
        live_objs = buffer.list_live_objects()
        self.assertEqual(live_objs, ["a", "b"])

    def test_undeclared_objs_err(self):
        parser = create_parser_from_string("x = a\nlive:\nz,")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        with self.assertRaises(ValueError):
            parser._parse_live(buffer)

    def test_invalid_token_err(self):
        parser = create_parser_from_string("x = a\nlive:\n=")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        with self.assertRaises(ValueError):
            parser._parse_live(buffer)

    def test_skips_newlines(self):
        parser = create_parser_from_string("x = a + b\nlive:\na,\nb,\n")
        buffer = InstructionBuffer()
        parser._parse_instructions(buffer)
        parser._parse_live(buffer)
        live_objs = buffer.list_live_objects()
        self.assertEqual(live_objs, ["a", "b"])

class TestParse(unittest.TestCase):
    def test_full_input(self):
        parser = create_parser_from_string("x = a + b\ny = x\nlive:\na, b,")
        buffer = parser.parse()
        occurred_vars = buffer.get_occurred_variables()
        instructions = buffer.list_instructions()
        live_objs = buffer.list_live_objects()
        self.assertEqual(occurred_vars, {"x", "a", "b", "y"})
        self.assertEqual(str(instructions[0]), "x = a + b")
        self.assertEqual(str(instructions[1]), "y = x")
        self.assertEqual(live_objs, ["a", "b"])

    def test_no_live(self):
        parser = create_parser_from_string("x = a + b\n")
        buffer = parser.parse()
        occurred_vars = buffer.get_occurred_variables()
        instructions = buffer.list_instructions()
        live_objs = buffer.list_live_objects()
        self.assertEqual(occurred_vars, {"x", "a", "b"})
        self.assertEqual(str(instructions[0]), "x = a + b")
        self.assertEqual(live_objs, [])
        
    def test_empty_file(self):
        parser = create_parser_from_string("")
        buffer = parser.parse()
        instructions = buffer.list_instructions()
        self.assertEqual(len(buffer.instructions), 0)
    
    def test_occurred_vars_on_buffer(self):
        parser = create_parser_from_string("x = a + b\nlive:\na,")
        buffer = parser.parse()
        occurred_vars = buffer.get_occurred_variables()
        self.assertEqual(occurred_vars, {"x", "a", "b"})

if __name__ == '__main__':
    unittest.main(verbosity=2)