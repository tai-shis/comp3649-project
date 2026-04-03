import unittest
from input.token import Token
from input.instruction import Instruction
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness


def make_buffer(instructions: list[Instruction], live_objects: list[str]) -> InstructionBuffer:
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


def make_binary(dest: str, op1: str, op1_type: int, operator: str, op2: str, op2_type: int) -> Instruction:
    """Helper to create a binary instruction."""
    return Instruction(0, Token(dest, 0), Token(op1, op1_type), Token(operator, 3), Token(op2, op2_type))


class TestLiveness(unittest.TestCase):

    def test_empty_buffer_returns_one_empty_dict(self):
        buf = make_buffer([], [])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result, [{}])

    def test_liveness_populated_on_init(self):
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        # liveness should be populated without any manual calls
        self.assertGreater(len(liveness.get_liveness()), 0)

    def test_no_live_objects(self):
        buf = make_buffer([], [])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        # Only the live section dict, which should be empty
        self.assertEqual(result[-1], {})

    def test_single_live_object(self):
        buf = make_buffer([], ["a"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result[-1], {"a": 1})

    def test_multiple_live_objects(self):
        buf = make_buffer([], ["a", "b"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result[-1], {"a": 1, "b": 1})

    """
    _mark_liveness() is private so we test it indirectly through
    get_liveness() on a Liveness object with a known buffer.
    """
    def test_assignment_no_carry_vars(self):
        # x = 42 (literal, no carry vars) — x defined, operand is literal so not in variables
        instr = make_assignment("x", "42", 2)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)  # defined

    def test_assignment_operand_in_carry_vars(self):
        # x = a, live: a — a should be live on the instruction line
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)   # defined
        self.assertEqual(instruction_line["a"], 1)   # live

    def test_assignment_operand_not_in_carry_vars(self):
        # x = a, no live objects — a should be unlive
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)   # defined
        self.assertEqual(instruction_line["a"], 2)   # unlive

    def test_binary_no_carry_vars(self):
        # x = a + b, no live objects — x defined, a and b unlive
        instr = make_binary("x", "a", 1, "+", "b", 1)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)   # defined
        self.assertEqual(instruction_line["a"], 2)   # unlive
        self.assertEqual(instruction_line["b"], 2)   # unlive

    def test_binary_both_operands_in_carry_vars(self):
        # x = a + b, live: a, b — a and b should be live
        instr = make_binary("x", "a", 1, "+", "b", 1)
        buf = make_buffer([instr], ["a", "b"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)   # defined
        self.assertEqual(instruction_line["a"], 1)   # live
        self.assertEqual(instruction_line["b"], 1)   # live

    def test_carry_vars_cleared_and_repopulated(self):
        # After processing x = a (with a live), carry vars should contain
        # only live/unlive vars from the current line, not stale ones
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        # The live section should only contain "a", not "x" (which was defined)
        live_section = result[-1]
        self.assertNotIn("x", live_section)

    def test_single_assignment(self):
        # x = a, live: a
        # Expected liveness: [{"a": 1}, {"x": 0, "a": 1}, {"a": 1}]
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result[0], {"x": 0, "a": 1})  # instruction line
        self.assertEqual(result[1], {"a": 1})           # live section

    def test_single_binary_instruction(self):
        # x = a + b, live: a, b — x defined, a and b live on instruction line
        instr = make_binary("x", "a", 1, "+", "b", 1)
        buf = make_buffer([instr], ["a", "b"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        instruction_line = result[0]
        self.assertEqual(instruction_line["x"], 0)  # defined
        self.assertEqual(instruction_line["a"], 1)  # live
        self.assertEqual(instruction_line["b"], 1)  # live

    def test_variable_defined_then_used(self):
        # x = a, y = x, live: x
        # x should be defined on line 0 and live on line 1
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "x", 1)
        buf = make_buffer([instr1, instr2], ["x"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result[0]["x"], 0)  # defined on line 0
        self.assertEqual(result[1]["x"], 1)  # live on line 1

    def test_variable_unlive_after_last_use(self):
        # x = a, y = b, live: b — a should be unlive on line 1
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "b", 1)
        buf = make_buffer([instr1, instr2], ["b"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertEqual(result[0]["a"], 2)  # a is unlive on second line

    def test_liveness_length_equals_instructions_plus_one(self):
        # 3 instructions + 1 live section = 4 entries
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "b", 1)
        instr3 = make_assignment("z", "c", 1)
        buf = make_buffer([instr1, instr2, instr3], [])
        liveness = Liveness(buf)
        self.assertEqual(len(liveness.get_liveness()), 4)

    def test_returns_list_of_dicts(self):
        buf = make_buffer([], ["a"])
        liveness = Liveness(buf)
        result = liveness.get_liveness()
        self.assertIsInstance(result, list)
        for entry in result:
            self.assertIsInstance(entry, dict)

    def test_correct_length_with_three_instructions(self):
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "b", 1)
        instr3 = make_assignment("z", "c", 1)
        buf = make_buffer([instr1, instr2, instr3], [])
        liveness = Liveness(buf)
        self.assertEqual(len(liveness.get_liveness()), 4)

    def test_defined_state_string(self):
        instr = make_assignment("x", "42", 2)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        info = liveness.liveness_info()
        self.assertIn("x: defined", info[0])

    def test_live_state_string(self):
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        info = liveness.liveness_info()
        self.assertIn("a: live", info[0])

    def test_unlive_state_string(self):
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        info = liveness.liveness_info()
        self.assertIn("a: unlive", info[0])

    def test_correct_format(self):
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], ["a"])
        liveness = Liveness(buf)
        info = liveness.liveness_info()
        for entry in info:
            self.assertTrue(entry.startswith("["))
            self.assertTrue(entry.endswith("]"))

    def test_correct_number_of_lines(self):
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "b", 1)
        buf = make_buffer([instr1, instr2], [])
        liveness = Liveness(buf)
        lines = str(liveness).strip().split("\n")
        self.assertEqual(len(lines), 3)  # 2 instructions + end of code block

    def test_end_of_code_block_line(self):
        instr = make_assignment("x", "a", 1)
        buf = make_buffer([instr], [])
        liveness = Liveness(buf)
        self.assertIn("End of code block:", str(liveness))

    def test_instruction_index_prefix(self):
        instr1 = make_assignment("x", "a", 1)
        instr2 = make_assignment("y", "b", 1)
        buf = make_buffer([instr1, instr2], [])
        liveness = Liveness(buf)
        lines = str(liveness).strip().split("\n")
        self.assertTrue(lines[0].startswith("0:"))
        self.assertTrue(lines[1].startswith("1:"))


if __name__ == "__main__":
    unittest.main(verbosity=2)