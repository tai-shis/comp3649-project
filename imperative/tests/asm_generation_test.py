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
        input = "a = a + 1\nt1 = a * 2\nb = t1 / 3\nlive: a, b"

        file = io.StringIO(input)
        scanner = Scanner(file)
        parser = Parser(scanner)
        
        return parser.parse()
    
    def _get_interference_graph(self, buffer: InstructionBuffer, liveness: Liveness) -> InterferenceGraph:
        '''
        Helper function to return an interference graph from a given instruction buffer and liveness.
        '''
        interference_graph = InterferenceGraph()
        interference_graph.build_graph(liveness, buffer.get_occured_variables())

        return interference_graph

    def test_init(self):
        '''
        Tests the ASMGenerator initialization.
        '''
        pass

    def test_reg_or_value_literal(self):
        '''
        Tests function responsible for returning the value from the literal
        that it is given. 
        '''
        pass

    def test_reg_or_value_variable(self):
        '''
        Tests function responsible for returning register for a variable from the
        Token it was given.
        '''
        pass

    def test_get_op_code_ADD(self):
        '''
        Tests the function responsible for returning the op-code for the ADD operator.
        '''
        buffer = self._get_buffer()

        liveness = Liveness(buffer)
        interference_graph = self._get_interference_graph(buffer, liveness)

        add_token: Token = Token("+", 3)
        generator: ASMGenerator = ASMGenerator(buffer, interference_graph)
        op_code = generator._get_op_code(add_token)

        self.assertEqual(op_code, "ADD")

    def test_get_op_code_SUB(self):
        '''
        Tests the function responsible for returning the op-code for the SUB operator.
        '''
        buffer = self._get_buffer()

        liveness = Liveness(buffer)
        interference_graph = self._get_interference_graph(buffer, liveness)

        sub_token: Token = Token("-", 3)
        generator: ASMGenerator = ASMGenerator(buffer, interference_graph)
        op_code = generator._get_op_code(sub_token)

        self.assertEqual(op_code, "SUB")

    def test_get_op_code_MUL(self):
        '''
        Tests the function responsible for returning the op-code for the MUL operator.
        '''
        buffer = self._get_buffer()

        liveness = Liveness(buffer)
        interference_graph = self._get_interference_graph(buffer, liveness)

        mul_token: Token = Token("*", 3)
        generator: ASMGenerator = ASMGenerator(buffer, interference_graph)
        op_code = generator._get_op_code(mul_token)

        self.assertEqual(op_code, "MUL")

    def test_get_op_code_DIV(self):
        '''
        Tests the function responsible for returning the op-code for the DIV operator.
        '''
        buffer = self._get_buffer()

        liveness = Liveness(buffer)
        interference_graph = self._get_interference_graph(buffer, liveness)

        div_token: Token = Token("/", 3)
        generator: ASMGenerator = ASMGenerator(buffer, interference_graph)
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