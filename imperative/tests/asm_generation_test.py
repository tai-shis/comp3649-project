import io
import unittest

from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.token import Token
from input.scanner import Scanner
from input.parser import Parser
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph
from generator.asm_generator import ASMGenerator

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

        return interference_graph
    
    def _get_generator(self) -> ASMGenerator:
        buffer = self._get_buffer()
        interference_graph = self._get_interference_graph(buffer)

        liveness = Liveness(buffer)
        interference_graph = InterferenceGraph()
        interference_graph.build_graph(liveness, buffer.get_occured_variables())

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

    def test_reg_or_value_literal(self):
        '''
        Tests function responsible for returning the value from the literal
        that it is given. 
        '''
        generator = self._get_generator()

        token = Token("1", 2)
        value = generator._get_reg_or_value(token)

        self.assertEqual(value, "#1")


    def test_reg_or_value_variable(self):
        '''
        Tests function responsible for returning register for a variable from the
        Token it was given.
        '''
        generator = self._get_generator()

        token = generator.buffer.instructions[0].dest
        expected_reg = "R1"
        value = generator._get_reg_or_value(token)

        print(f"\n {token.type}")
        print(f"\n {token.value}")
        print(f"\n {generator.buffer.instructions[0]}")
        print(f"\n {generator.register_colors}")
        self.assertEqual(value, expected_reg)

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

    def test_generate_instruction_asm(self):
        '''
        Tests the function responsible for generating ASM code for a given instruction.
        '''
        pass

    def test_generate_assembly(self):
        '''
        Tests the function responsible for generating all ASM code from a given input file.
        '''
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)