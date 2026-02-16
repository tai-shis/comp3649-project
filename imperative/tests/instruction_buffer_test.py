import array
import io
import unittest
from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.scanner import Token
import llist

class TestInstructionBuffer(unittest.TestCase):

    def test_add_instruction_TYPE0(self):
        instruction: Instruction = Instruction(0, "a", "a", "+", "1")
        ib: InstructionBuffer = InstructionBuffer()
        ib.add_instruction(instruction)

        self.assertEqual(ib.instructions[0], instruction)
        self.assertEqual(ib.instructions[0].type, 0)

    def test_add_instruction_TYPE1(self):
        instruction: Instruction = Instruction(type=1, dest="a", operator="+", operand2="1")
        ib: InstructionBuffer = InstructionBuffer()
        ib.add_instruction(instruction)

        self.assertEqual(ib.instructions[0], instruction)
        self.assertEqual(ib.instructions[0].type, 1)

    def test_add_instruction_TYPE2(self):
        instruction: Instruction = Instruction(type=2, dest="a", operand1="1")
        ib: InstructionBuffer = InstructionBuffer()
        ib.add_instruction(instruction)

        self.assertEqual(ib.instructions[0], instruction)
        self.assertEqual(ib.instructions[0].type, 2)

    def test_add_live_object(self):
        lo: str = "a"
        ib: InstructionBuffer = InstructionBuffer()
        ib.add_live_object(lo)

        self.assertEqual(ib.live_objects[0], lo)

    def test_list_instructions(self):
        ins0: Instruction = Instruction(
            0, 
            Token("a", 0),
            Token("a", 1),
            Token("+", 3),
            Token("1", 2))
        ins1: Instruction = Instruction(
            0,
            Token("b", 0),
            Token("a", 1),
            Token("-", 3),
            Token("6", 2))
        ins2: Instruction = Instruction(
            0,
            Token("t1", 0),
            Token("b", 1),
            Token("/", 3),
            Token("2", 2))
        ins3: Instruction = Instruction(
            0,
            Token("prod_a", 0),
            Token("a", 1),
            Token("*", 3),
            Token("6",2))
        ins4: Instruction = Instruction(
            1,
            Token("c", 0),
            Token("1", 2),
            Token("+", 3),
            Token("2", 2))

        ib: InstructionBuffer = InstructionBuffer()
        ib.add_instruction(ins0)
        ib.add_instruction(ins1)
        ib.add_instruction(ins2)
        ib.add_instruction(ins3)
        ib.add_instruction(ins4)

        ib_list: list[str] = ib.list_instructions()

        self.assertEqual(str(ib_list[0]), str(ins0))
        self.assertEqual(str(ib_list[1]), str(ins1))
        self.assertEqual(str(ib_list[2]), str(ins2))
        self.assertEqual(str(ib_list[3]), str(ins3))
        self.assertEqual(str(ib_list[4]), str(ins4))



    def test_list_live_objects(self):
        lo0: str = "a"
        lo1: str = "b"
        lo2: str = "c"
        ib: InstructionBuffer = InstructionBuffer()
        ib.add_live_object(lo0)
        ib.add_live_object(lo1)
        ib.add_live_object(lo2)

        li_list: list[str] = ib.list_live_objects()

        self.assertEqual(li_list[0], "a")
        self.assertEqual(li_list[1], "b")
        self.assertEqual(li_list[2], "c")

if __name__ == "__main__":
    unittest.main(verbosity=2)