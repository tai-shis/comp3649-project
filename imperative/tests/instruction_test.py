import unittest
from input.token import Token
from input.instruction import Instruction


class TestInstruction(unittest.TestCase):

    def test_binary_operator_construction(self):
        dest = Token("x", 0)
        operand1 = Token("a", 1)
        operator = Token("+", 3)
        operand2 = Token("b", 1)
        instr = Instruction(0, dest, operand1, operator, operand2)

        self.assertEqual(instr.type, 0)
        self.assertEqual(instr.dest, dest)
        self.assertEqual(instr.operand1, operand1)
        self.assertEqual(instr.operator, operator)
        self.assertEqual(instr.operand2, operand2)

    def test_unary_operator_construction(self):
        dest = Token("x", 0)
        operator = Token("-", 3)
        operand2 = Token("a", 1)
        instr = Instruction(1, dest, operator=operator, operand2=operand2)

        self.assertEqual(instr.type, 1)
        self.assertEqual(instr.dest, dest)
        self.assertEqual(instr.operator, operator)
        self.assertEqual(instr.operand2, operand2)
        self.assertIsNone(instr.operand1)

    def test_assignment_construction(self):
        dest = Token("x", 0)
        operand1 = Token("a", 1)
        instr = Instruction(2, dest, operand1)

        self.assertEqual(instr.type, 2)
        self.assertEqual(instr.dest, dest)
        self.assertEqual(instr.operand1, operand1)
        self.assertIsNone(instr.operator)
        self.assertIsNone(instr.operand2)

    def test_invalid_type_construction(self):
        dest = Token("x", 0)
        instr = Instruction(-1, dest)

        self.assertEqual(instr.type, -1)
        self.assertEqual(instr.dest, dest)
        self.assertIsNone(instr.operand1)
        self.assertIsNone(instr.operator)
        self.assertIsNone(instr.operand2)

    def test_str_binary_operator(self):
        instr = Instruction(0, Token("x", 0), Token("a", 1), Token("+", 3), Token("b", 1))
        self.assertEqual(str(instr), "x = a + b")

    def test_str_unary_operator(self):
        instr = Instruction(1, Token("x", 0), operator=Token("-", 3), operand2=Token("a", 1))
        self.assertEqual(str(instr), "x = -a")

    def test_str_assignment(self):
        instr = Instruction(2, Token("x", 0), Token("42", 2))
        self.assertEqual(str(instr), "x = 42")

    def test_binary_all_variables(self):
        dest = Token("x", 0)
        operand1 = Token("a", 1)
        operand2 = Token("b", 1)
        instr = Instruction(0, dest, operand1, Token("+", 3), operand2)

        result = instr.get_variables()
        self.assertEqual(result, [dest, operand1, operand2])

    def test_binary_literal_operands(self):
        dest = Token("x", 0)
        operand1 = Token("1", 2)
        operand2 = Token("2", 2)
        instr = Instruction(0, dest, operand1, Token("+", 3), operand2)

        result = instr.get_variables()
        self.assertEqual(result, [dest])

    def test_binary_mixed_operands(self):
        dest = Token("x", 0)
        operand1 = Token("a", 1)
        operand2 = Token("2", 2)
        instr = Instruction(0, dest, operand1, Token("+", 3), operand2)

        result = instr.get_variables()
        self.assertEqual(result, [dest, operand1])

    def test_unary_variable_operand(self):
        dest = Token("x", 0)
        operand2 = Token("a", 1)
        instr = Instruction(1, dest, operator=Token("-", 3), operand2=operand2)

        result = instr.get_variables()
        self.assertEqual(result, [dest, operand2])

    def test_unary_literal_operand(self):
        dest = Token("x", 0)
        operand2 = Token("42", 2)
        instr = Instruction(1, dest, operator=Token("-", 3), operand2=operand2)

        result = instr.get_variables()
        self.assertEqual(result, [dest])

    def test_assignment_variable_operand(self):
        dest = Token("x", 0)
        operand1 = Token("a", 1)
        instr = Instruction(2, dest, operand1)

        result = instr.get_variables()
        self.assertEqual(result, [dest, operand1])

    def test_assignment_literal_operand(self):
        dest = Token("x", 0)
        operand1 = Token("42", 2)
        instr = Instruction(2, dest, operand1)

        result = instr.get_variables()
        self.assertEqual(result, [dest])


if __name__ == "__main__":
    unittest.main(verbosity=2)