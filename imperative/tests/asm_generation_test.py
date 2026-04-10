import os
import unittest
from unittest.mock import MagicMock

from generator.asm_generator import ASMGenerator
from generator.asm_instruction import ASMInstruction
from input.instruction import Instruction
from input.instruction_buffer import InstructionBuffer
from input.token import Token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_graph(colors: dict[str, int | None]) -> MagicMock:
    """Helper to build a mock InterferenceGraph with a given colors dict."""
    graph = MagicMock()
    graph.colors = colors
    return graph


def make_buffer(raw_instructions: list[Instruction]) -> InstructionBuffer:
    """Helper to build an InstructionBuffer from a list of Instructions."""
    buf = InstructionBuffer()
    for instr in raw_instructions:
        buf.add_instruction(instr)
    return buf


def make_generator(instructions: list[Instruction], colors: dict[str, int | None]) -> ASMGenerator:
    """Helper that combines make_buffer and make_graph into an ASMGenerator."""
    return ASMGenerator(make_buffer(instructions), make_graph(colors))


def make_binary(dest: str, op1: str, op1_type: int,
                operator: str, op2: str, op2_type: int) -> Instruction:
    """Helper to create a binary (type-0) instruction."""
    return Instruction(
        0,
        Token(dest, 0),
        Token(op1, op1_type),
        Token(operator, 3),
        Token(op2, op2_type),
    )


def make_unary(dest: str, operator: str, operand: str, operand_type: int) -> Instruction:
    """Helper to create a unary (type-1) instruction."""
    return Instruction(
        1,
        Token(dest, 0),
        operator=Token(operator, 3),
        operand2=Token(operand, operand_type),
    )


def make_assignment(dest: str, operand: str, operand_type: int) -> Instruction:
    """Helper to create an assignment (type-2) instruction."""
    return Instruction(2, Token(dest, 0), Token(operand, operand_type))


# ---------------------------------------------------------------------------
# Construction tests
# ---------------------------------------------------------------------------

class TestASMGeneratorConstruction(unittest.TestCase):

    def test_fields_initialized(self):
        buf = make_buffer([])
        graph = make_graph({"a": 0})
        gen = ASMGenerator(buf, graph)

        self.assertEqual(gen.generated_asm, [])
        self.assertEqual(gen.register_colors, graph.colors)
        self.assertIs(gen.buffer, buf)

    def test_opcodes_initialized(self):
        gen = make_generator([], {})
        expected = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
        self.assertEqual(gen.opcodes, expected)


# ---------------------------------------------------------------------------
# _get_reg_or_value() tests
# ---------------------------------------------------------------------------

class TestGetRegOrValue(unittest.TestCase):

    def test_literal_token_returns_hash_prefixed(self):
        gen = make_generator([], {})
        token = Token("42", 2)
        self.assertEqual(gen._get_reg_or_value(token), "#42")

    def test_variable_assigned_to_r0(self):
        gen = make_generator([], {"a": 0})
        token = Token("a", 1)
        self.assertEqual(gen._get_reg_or_value(token), "R0")

    def test_variable_assigned_to_r2(self):
        gen = make_generator([], {"b": 2})
        token = Token("b", 1)
        self.assertEqual(gen._get_reg_or_value(token), "R2")

    def test_variable_with_no_register_raises_error(self):
        gen = make_generator([], {})
        token = Token("z", 1)
        with self.assertRaises(ValueError):
            gen._get_reg_or_value(token)

    def test_variable_with_none_color_returns_value(self):
        gen = make_generator([], {"a": None})
        token = Token("a", 1)
        self.assertEqual(gen._get_reg_or_value(token), "a")


# ---------------------------------------------------------------------------
# _get_op_code() tests
# ---------------------------------------------------------------------------

class TestGetOpCode(unittest.TestCase):

    def test_addition(self):
        gen = make_generator([], {})
        self.assertEqual(gen._get_op_code(Token("+", 3)), "ADD")

    def test_subtraction(self):
        gen = make_generator([], {})
        self.assertEqual(gen._get_op_code(Token("-", 3)), "SUB")

    def test_multiplication(self):
        gen = make_generator([], {})
        self.assertEqual(gen._get_op_code(Token("*", 3)), "MUL")

    def test_division(self):
        gen = make_generator([], {})
        self.assertEqual(gen._get_op_code(Token("/", 3)), "DIV")


# ---------------------------------------------------------------------------
# _generate_instruction_asm() tests
# ---------------------------------------------------------------------------

class TestGenerateInstructionAsm(unittest.TestCase):

    def test_binary_operator(self):
        instr = make_binary("x", "a", 1, "+", "b", 1)
        gen = make_generator([instr], {"x": 0, "a": 1, "b": 2})
        result = gen._generate_instruction_asm(instr)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "a")
        self.assertEqual(result[0].op2, "R0")
        self.assertEqual(result[1].op_code, "ADD")
        self.assertEqual(result[1].op1, "R2")
        self.assertEqual(result[1].op2, "R0")

    def test_binary_with_literal_operand(self):
        instr = Instruction(
            0,
            Token("x", 0),
            Token("1", 2),
            Token("+", 3),
            Token("2", 2),
        )
        gen = make_generator([instr], {"x": 0})
        result = gen._generate_instruction_asm(instr)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "1")
        self.assertEqual(result[0].op2, "R0")
        self.assertEqual(result[1].op_code, "ADD")
        self.assertEqual(result[1].op1, "#2")
        self.assertEqual(result[1].op2, "R0")

    def test_unary_negation(self):
        instr = make_unary("x", "-", "a", 1)
        gen = make_generator([instr], {"x": 1, "a": 0})
        result = gen._generate_instruction_asm(instr)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "a")
        self.assertEqual(result[0].op2, "R1")
        self.assertEqual(result[1].op_code, "MUL")
        self.assertEqual(result[1].op1, "#-1")
        self.assertEqual(result[1].op2, "R1")

    def test_assignment_from_variable(self):
        instr = make_assignment("x", "a", 1)
        gen = make_generator([instr], {"x": 1, "a": 0})
        result = gen._generate_instruction_asm(instr)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "R0")
        self.assertEqual(result[0].op2, "R1")

    def test_assignment_from_literal(self):
        instr = make_assignment("x", "42", 2)
        gen = make_generator([instr], {"x": 0})
        result = gen._generate_instruction_asm(instr)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "#42")
        self.assertEqual(result[0].op2, "R0")

    def test_invalid_instruction_type_returns_empty(self):
        instr = Instruction(-1, Token("x", 0))
        gen = make_generator([], {})
        result = gen._generate_instruction_asm(instr)
        self.assertEqual(result, [])

    def test_returns_list_of_asm_instructions(self):
        instr = make_assignment("x", "a", 1)
        gen = make_generator([instr], {"x": 0, "a": 1})
        result = gen._generate_instruction_asm(instr)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, ASMInstruction)


# ---------------------------------------------------------------------------
# generate_assembly() tests
# ---------------------------------------------------------------------------

class TestGenerateAssembly(unittest.TestCase):

    def _tmp_path(self, filename: str) -> str:
        return os.path.join("output", "test_tmp", filename)

    def test_single_binary_instruction(self):
        instr = make_binary("x", "a", 1, "+", "b", 1)
        gen = make_generator([instr], {"x": 0, "a": 1, "b": 2})
        result = gen.generate_assembly(self._tmp_path("single_binary.asm"))
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ASMInstruction)
        self.assertIsInstance(result[1], ASMInstruction)

    def test_single_assignment_instruction(self):
        instr = make_assignment("x", "a", 1)
        gen = make_generator([instr], {"x": 1, "a": 0})
        result = gen.generate_assembly(self._tmp_path("single_assign.asm"))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].op_code, "MOV")

    def test_multiple_instructions_correct_total(self):
        instrs = [
            make_binary("x", "a", 1, "+", "b", 1),   # 2 ASM instructions
            make_assignment("y", "x", 1),              # 1 ASM instruction
            make_unary("z", "-", "y", 1),              # 2 ASM instructions
        ]
        colors = {"x": 0, "a": 1, "b": 2, "y": 3, "z": 4}
        gen = make_generator(instrs, colors)
        result = gen.generate_assembly(self._tmp_path("multiple.asm"))
        self.assertEqual(len(result), 5)

    def test_returns_list(self):
        instr = make_assignment("x", "42", 2)
        gen = make_generator([instr], {"x": 0})
        result = gen.generate_assembly(self._tmp_path("returns_list.asm"))
        self.assertIsInstance(result, list)


# ---------------------------------------------------------------------------
# _output_to_file() tests  (exercised via generate_assembly)
# ---------------------------------------------------------------------------

class TestOutputToFile(unittest.TestCase):

    def setUp(self):
        self.output_dir = os.path.join("output", "test_asm_output")
        os.makedirs(self.output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self.output_dir, filename)

    def test_file_created(self):
        instr = make_binary("x", "a", 1, "+", "b", 1)
        gen = make_generator([instr], {"x": 0, "a": 1, "b": 2})
        path = self._path("created.asm")
        gen.generate_assembly(path)
        self.assertTrue(os.path.exists(path))

    def test_correct_file_format(self):
        instr = make_binary("x", "a", 1, "+", "b", 1)
        gen = make_generator([instr], {"x": 0, "a": 1, "b": 2})
        path = self._path("format.asm")
        gen.generate_assembly(path)

        with open(path) as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            # Each line should be "OPCODE op1,op2"
            parts = line.split(" ", 1)
            self.assertEqual(len(parts), 2, f"Unexpected format: {line!r}")
            self.assertIn(",", parts[1], f"Missing comma in operands: {line!r}")

    def test_creates_missing_directories(self):
        subdir_path = os.path.join("output", "test_asm_subdir", "nested", "test.asm")
        instr = make_assignment("x", "42", 2)
        gen = make_generator([instr], {"x": 0})
        gen.generate_assembly(subdir_path)
        self.assertTrue(os.path.exists(subdir_path))

    def test_correct_number_of_lines(self):
        # 2 binary instructions → 4 ASM lines
        instrs = [
            make_binary("x", "a", 1, "+", "b", 1),
            make_binary("y", "c", 1, "*", "d", 1),
        ]
        colors = {"x": 0, "a": 1, "b": 2, "y": 3, "c": 4, "d": 5}
        gen = make_generator(instrs, colors)
        path = self._path("line_count.asm")
        gen.generate_assembly(path)

        with open(path) as f:
            lines = [l for l in f.readlines() if l.strip()]

        self.assertEqual(len(lines), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)