import unittest
from generator.asm_instruction import ASMInstruction

class TestASMInstruction(unittest.TestCase):

    def test_MOV_instruction(self):
        ins = ASMInstruction("MOV", "R0", "R1")
        self.assertEqual(str(ins), "MOV R0,R1")

    def test_ADD_instruction(self):
        ins = ASMInstruction("ADD", "#1", "R0")
        self.assertEqual(str(ins), "ADD #1,R0")

    def test_SUB_instruction(self):
        ins = ASMInstruction("SUB", "R1", "R0")
        self.assertEqual(str(ins), "SUB R1,R0")

    def test_MUL_instruction(self):
        ins = ASMInstruction("MUL", "#-1", "R0")
        self.assertEqual(str(ins), "MUL #-1,R0")

    def test_DIV_instruction(self):
        ins = ASMInstruction("DIV", "R2", "R0")
        self.assertEqual(str(ins), "DIV R2,R0")

    def test_literal(self):
        ins = ASMInstruction("MOV", "#29", "R0")
        self.assertEqual(ins.op1, "#29")

if __name__ == '__main__':
    unittest.main(verbosity=2)
    