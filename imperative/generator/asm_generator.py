import os

from generator.asm_instruction import ASMInstruction
from intermediate.interference_graph import InterferenceGraph
from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.token import Token

class ASMGenerator:
    def __init__(self, instruction_buffer: InstructionBuffer, interference_graph: InterferenceGraph):
        self.buffer: InstructionBuffer = instruction_buffer
        self.register_colors: dict[str, int | None] = interference_graph.colors

        self.generated_asm: list[ASMInstruction] = []
        
        self.opcodes = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
        }

    def _get_reg_or_value(self, token: Token) -> str:
        """
        Converts a Token into its assembly operand string.

        Literals are prefixed with '#'; variables are resolved to their assigned register.

        :param token: The token to convert.
        :type token: Token
        :return: The assembly operand string.
        :rtype: str
        """
        if (token.type == 2): # 'literal' Token type
            return f"#{token.value}"

        if token.value not in self.register_colors:
            raise ValueError(f"Error: Variable {str(token.value)} has no assigned register.")

        register = self.register_colors[token.value]
        if register is None:
            return str(token.value)

        return f"R{register}"
        

    def _get_op_code(self, operator: Token) -> str:
        """
        Returns the assembly op-code for the given operator token.

        :param operator: The operator token.
        :type operator: Token
        :return: The op-code string (e.g. 'ADD', 'SUB').
        :rtype: str
        """

        return self.opcodes[operator.value]
                
    def _generate_instruction_asm(self, instruction: Instruction) -> list[ASMInstruction]:
        """
        Generates the assembly instructions for a single three-address instruction.

        :param instruction: The instruction to generate assembly for.
        :type instruction: Instruction
        :return: The list of assembly instructions.
        :rtype: list[ASMInstruction]
        """

        match instruction.type:
            case 0: # Binary Operator
                
                dest = self._get_reg_or_value(instruction.dest)
                op1 = instruction.operand1.value
                op2 = self._get_reg_or_value(instruction.operand2)
                op_code = self._get_op_code(instruction.operator)
                
                operation1 = ASMInstruction("MOV", op1, dest)
                operation2 = ASMInstruction(op_code, op2, dest)
                return [operation1, operation2]

            case 1: # Unary Operator
                # Example: Assume b is already live and stored in R0
                # x = -b
                # MOV R0, R1 ; Storing x in R1
                # MUL #-1,R1 ; taking inverse of b and storing in x (value in R0)

                dest = self._get_reg_or_value(instruction.dest)
                source = instruction.operand2.value
                op_symbol = instruction.operator.value

                if (op_symbol == '-'):
                    # Negation: MOV source into dest, then multiply by -1
                    operation1 = ASMInstruction("MOV", source, dest)
                    operation2 = ASMInstruction("MUL", "#-1", dest)

                    return [operation1, operation2]

                return [ASMInstruction("MOV", source, dest)]
                
            case 2: # Assignment
                dest = self._get_reg_or_value(instruction.dest)
                source = self._get_reg_or_value(instruction.operand1)
                return [ASMInstruction("MOV", source, dest)]
            
            case _:
                return []
    
    def _output_to_file(self, input_filename: str) -> None:
        """
        Writes the generated assembly instructions to the given file path.
        """
        output_name = f"{input_filename}"
        
        os.makedirs(os.path.dirname(output_name), exist_ok=True)

        with open(output_name, "w") as f:
            for instruction in self.generated_asm:
                instruction_str = instruction.op_code + " " + instruction.op1 + "," + instruction.op2
                f.write(f"{instruction_str}\n")

    def generate_assembly(self, input_filename: str) -> list[ASMInstruction]:
        """
        Generates assembly for every instruction in the buffer and writes it to a file.

        :return: The list of generated assembly instructions.
        :rtype: list[ASMInstruction]
        """
        for instruction in self.buffer.instructions:
            next_instructions: list[ASMInstruction] = self._generate_instruction_asm(instruction)
            self.generated_asm.extend(next_instructions)

        self._output_to_file(input_filename)

        return self.generated_asm
    