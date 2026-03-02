import io
from multiprocessing import Value
import unittest
import os

from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.token import Token
from input.scanner import Scanner
from input.parser import Parser
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph
from generator.asm_generator import ASMGenerator
from generator.asm_instruction import ASMInstruction

class TestASMGeneration(unittest.TestCase):

    def _get_buffer(self) -> InstructionBuffer:
        '''
        Helper function create an instruction buffer
        '''
        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b\n"

        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        
        return parser.parse()
    
    def _get_interference_graph(self, buffer: InstructionBuffer) -> InterferenceGraph:
        '''
        Helper function to return an interference graph from a given instruction buffer and liveness.
        '''
        liveness = Liveness(buffer)
        interference_graph = InterferenceGraph()
        interference_graph.build_graph(liveness, buffer.get_occured_variables())
        interference_graph.color_graph(3)

        return interference_graph
    
    def _get_generator(self) -> ASMGenerator:
        buffer = self._get_buffer()
        interference_graph = self._get_interference_graph(buffer)

        return ASMGenerator(buffer, interference_graph)


    def test_init(self):
        '''
        Tests the ASMGenerator initialization.
        '''
        buffer = self._get_buffer()
        interference_graph = self._get_interference_graph(buffer)
        generator = ASMGenerator(buffer, interference_graph)

        self.assertEqual(generator.buffer, buffer)
        self.assertEqual(generator.register_colors, interference_graph.colors)

    def test_reg_or_value_no_register(self):
        '''
        Tests that the generator returns the variable name if no register was
        assigned in the interference graph.
        '''
        generator = self._get_generator()
        token = Token("none", 1)

        if ("none" in generator.register_colors):
            del generator.register_colors["none"]

        with self.assertRaises(ValueError):
            generator._get_reg_or_value(token)


    def test_reg_or_value_literal(self):
        '''
        Tests function responsible for returning the value from the literal
        that it is given. 
        '''
        generator = self._get_generator()

        token = Token("1", 2)
        value = generator._get_reg_or_value(token)

        self.assertEqual(value, "#1")

    def test_get_op_code_ADD(self):
        '''
        Tests the function responsible for returning the op-code for the ADD operator.
        '''
        add_token: Token = Token("+", 3)
        generator = self._get_generator()
        op_code = generator._get_op_code(add_token)

        self.assertEqual(op_code, "ADD")

    def test_get_op_code_SUB(self):
        '''
        Tests the function responsible for returning the op-code for the SUB operator.
        '''
        sub_token: Token = Token("-", 3)
        generator = self._get_generator()
        op_code = generator._get_op_code(sub_token)

        self.assertEqual(op_code, "SUB")

    def test_get_op_code_MUL(self):
        '''
        Tests the function responsible for returning the op-code for the MUL operator.
        '''
        mul_token: Token = Token("*", 3)
        generator = self._get_generator()
        op_code = generator._get_op_code(mul_token)

        self.assertEqual(op_code, "MUL")

    def test_get_op_code_DIV(self):
        '''
        Tests the function responsible for returning the op-code for the DIV operator.
        '''
        div_token: Token = Token("/", 3)
        generator = self._get_generator()
        op_code = generator._get_op_code(div_token)

        self.assertEqual(op_code, "DIV")

    def test_generate_instruction_binary(self):
        '''
        Tests the function responsible for generating ASM code for a given instruction.
        '''
        generator = self._get_generator()

        '''
        Testing first instruction in the buffer
        a = a + 1
        ''' 
        instruction = generator.buffer.instructions[0]
        asm = generator._generate_instruction_asm(instruction)
        register = f'R{generator.register_colors["a"]}'
        expected_asm = [ASMInstruction("MOV", "a", register), ASMInstruction("ADD", "#1", register)]
        
        self.assertEqual(asm[0].op_code, expected_asm[0].op_code)
        self.assertEqual(asm[0].op1, expected_asm[0].op1)
        self.assertEqual(asm[0].op2, expected_asm[0].op2)

        self.assertEqual(asm[1].op_code, expected_asm[1].op_code)
        self.assertEqual(asm[1].op1, expected_asm[1].op1)
        self.assertEqual(asm[1].op2, expected_asm[1].op2)
        


    def test_generate_instruction_unary(self):
        generator = self._get_generator()
        # Testing a = -b
        instruction = Instruction(
            1,
            dest=Token('a', 0),
            operator=Token('-', 3),
            operand2=Token('b', 1))
        asm = generator._generate_instruction_asm(instruction)
        register = f"R{generator.register_colors["a"]}"
        expected_asm = [ASMInstruction("MOV", "b", register), ASMInstruction("MUL", "#-1", register)]
        self.assertEqual(asm[0].op_code, expected_asm[0].op_code)
        self.assertEqual(asm[0].op1, expected_asm[0].op1)
        self.assertEqual(asm[0].op2, expected_asm[0].op2)
        
        self.assertEqual(asm[1].op_code, expected_asm[1].op_code)
        self.assertEqual(asm[1].op1, expected_asm[1].op1)
        self.assertEqual(asm[1].op2, expected_asm[1].op2)

    def test_generate_instruction_assignment(self):
        generator = self._get_generator()
        # Testing a = 1
        instruction = Instruction(
            2,
            dest=Token('a',0),
            operand1=Token('1',2))
        asm = generator._generate_instruction_asm(instruction)
        register = f"R{generator.register_colors["a"]}"
        expected_asm = [ASMInstruction("MOV", "#1", register)]
        
        self.assertEqual(asm[0].op_code, expected_asm[0].op_code)
        self.assertEqual(asm[0].op1, expected_asm[0].op1)
        self.assertEqual(asm[0].op2, expected_asm[0].op2)

    def test_output_file_content(self):
        '''
        Checks if the assembly.s file is created and contains the expected contents.
        '''
        path = "./generated/assembly.s"

        generator = self._get_generator()
        generator.generate_assembly(path)

        # Make sure the file was created
        self.assertTrue(os.path.exists(path))

        # Testing 'a = a + 1' which should have resulted in a MOV and an ADD operation
        # Test line 1
        with open(path, "r") as f:
            lines = f.readlines()
            # Verify that the first line is something like "MOV, a,R0" (register can vary)
            register = f"R{generator.register_colors["a"]}"
            expected_line = f"MOV a,{register}\n"
            self.assertEqual(lines[0], expected_line)

        # Test line 2
        with open(path, "r") as f:
            lines = f.readlines()
            # Verify that the first line is something like "ADD, #1,R0" (register can vary)
            register = f"R{generator.register_colors["a"]}"
            expected_line = f"ADD #1,{register}\n"
            self.assertEqual(lines[1], expected_line)


    def test_asm_instruction_object_integrity(self):
        '''
        Checks that the ASMInstruction objects have the correct op_code, op1, op2
        after being created.
        '''
        generator = self._get_generator()
        # a = a + 1
        instruction = generator.buffer.instructions[0]
        asm_objects = generator._generate_instruction_asm(instruction)
        
        register = f"R{generator.register_colors["a"]}"
        
        # Check MOV object
        self.assertEqual(asm_objects[0].op_code, "MOV")
        self.assertEqual(asm_objects[0].op1, "a")
        self.assertEqual(asm_objects[0].op2, register)
        
        # Check ADD object
        self.assertEqual(asm_objects[1].op_code, "ADD")
        self.assertEqual(asm_objects[1].op1, "#1")
        self.assertEqual(asm_objects[1].op2, register)

    # def test_generate_assembly(self):
    #     '''
    #     Tests the function responsible for generating all ASM code from a given input file.
    #     '''
    #     generator = self._get_generator()
    #     asm_list = generator.generate_assembly()
    #     print(asm_list)
    #     # NOTE: Add proper test for this at some point. But from the looks of things
    #     # it is printing out what is expected

if __name__ == '__main__':
    unittest.main(verbosity=2)