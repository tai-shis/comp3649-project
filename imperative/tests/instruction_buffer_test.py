import unittest
from llist import dllist
from input.token import Token
from input.instruction import Instruction
from input.instruction_buffer import InstructionBuffer


def make_instruction(type: int) -> Instruction:
    dest = Token("x", 0)
    operand1 = Token("a", 1)
    operator = Token("+", 3)
    operand2 = Token("b", 1)
    return Instruction(type, dest, operand1, operator, operand2)


class TestInstructionBuffer(unittest.TestCase):

    def test_instructions_empty_on_construction(self):
        buf = InstructionBuffer()
        self.assertIsInstance(buf.instructions, dllist)
        self.assertEqual(len(buf.instructions), 0)

    def test_live_objects_empty_on_construction(self):
        buf = InstructionBuffer()
        self.assertIsInstance(buf.live_objects, dllist)
        self.assertEqual(len(buf.live_objects), 0)

    def test_occurred_variables_empty_on_construction(self):
        buf = InstructionBuffer()
        self.assertIsInstance(buf.occurred_variables, set)
        self.assertEqual(buf.occurred_variables, set())

    def test_add_single_instruction(self):
        buf = InstructionBuffer()
        instr = make_instruction(0)
        buf.add_instruction(instr)
        self.assertEqual(buf.list_instructions(), [instr])

    def test_add_multiple_instructions_preserves_order(self):
        buf = InstructionBuffer()
        instr1 = make_instruction(0)
        instr2 = make_instruction(1)
        instr3 = make_instruction(2)
        buf.add_instruction(instr1)
        buf.add_instruction(instr2)
        buf.add_instruction(instr3)
        self.assertEqual(buf.list_instructions(), [instr1, instr2, instr3])

    def test_add_single_live_object(self):
        buf = InstructionBuffer()
        buf.add_live_object("a")
        self.assertEqual(buf.list_live_objects(), ["a"])

    def test_add_multiple_live_objects_preserves_order(self):
        buf = InstructionBuffer()
        buf.add_live_object("a")
        buf.add_live_object("b")
        buf.add_live_object("c")
        self.assertEqual(buf.list_live_objects(), ["a", "b", "c"])

    def test_list_instructions_empty_buffer(self):
        buf = InstructionBuffer()
        self.assertEqual(buf.list_instructions(), [])

    def test_list_instructions_populated_buffer(self):
        buf = InstructionBuffer()
        instr1 = make_instruction(0)
        instr2 = make_instruction(2)
        buf.add_instruction(instr1)
        buf.add_instruction(instr2)
        result = buf.list_instructions()
        self.assertEqual(result, [instr1, instr2])

    def test_list_live_objects_empty_buffer(self):
        buf = InstructionBuffer()
        self.assertEqual(buf.list_live_objects(), [])

    def test_list_live_objects_populated_buffer(self):
        buf = InstructionBuffer()
        buf.add_live_object("a")
        buf.add_live_object("b")
        self.assertEqual(buf.list_live_objects(), ["a", "b"])

    def test_get_instructions_returns_dllist(self):
        buf = InstructionBuffer()
        instr = make_instruction(0)
        buf.add_instruction(instr)
        result = buf.get_instructions()
        self.assertIsInstance(result, dllist)

    def test_get_instructions_contains_added_instruction(self):
        buf = InstructionBuffer()
        instr = make_instruction(0)
        buf.add_instruction(instr)
        result = buf.get_instructions()
        self.assertEqual(result.first.value, instr)

    def test_get_live_objects_returns_dllist(self):
        buf = InstructionBuffer()
        buf.add_live_object("a")
        result = buf.get_live_objects()
        self.assertIsInstance(result, dllist)

    def test_get_live_objects_contains_added_object(self):
        buf = InstructionBuffer()
        buf.add_live_object("a")
        result = buf.get_live_objects()
        self.assertEqual(result.first.value, "a")

    def test_get_occurred_variables_empty_on_construction(self):
        buf = InstructionBuffer()
        self.assertEqual(buf.get_occurred_variables(), set())

    def test_set_occurred_variables(self):
        buf = InstructionBuffer()
        buf.set_occurred_variables({"a", "b"})
        self.assertEqual(buf.get_occurred_variables(), {"a", "b"})

    def test_get_occurred_variables_after_set(self):
        buf = InstructionBuffer()
        buf.set_occurred_variables({"x"})
        self.assertEqual(buf.get_occurred_variables(), {"x"})


if __name__ == "__main__":
    unittest.main()