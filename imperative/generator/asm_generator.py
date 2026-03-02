from generator.asm_instruction import ASMInstruction
from intermediate.interference_graph import InterferenceGraph
from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.token import Token

class ASMGenerator:
    def __init__(self, instruction_buffer: InstructionBuffer, interference_graph: InterferenceGraph):
        self.buffer: InstructionBuffer = instruction_buffer
        self.register_colors: dict[str, int | None] = interference_graph.colors

        # This will be formatted like ["MOV a,R0", "ADD #1,R0"] where each string entry can be separated by a "\n" when being printed
        # out to the console of output file
        self.generated_asm: list[ASMInstruction] = []
        
        self.opcodes = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
        }

    def _get_reg_or_value(self, token: Token) -> str:
        '''
        Converts a Token into its assembly string representation.

        If the Token is a literal/constant, it returns the value with '#' prefixed.
        If the Token is a variable, it finds which register the variable is assigned to
        and returns that.

        :param token: The token to convert
        :type token: Token
        :return: The assembly operand string
        :rtype: str  
        '''
        if (token.type == 2): # 'literal' Token type
            return f"#{token.value}"

        if token.value not in self.register_colors:
            raise ValueError(f"Error: Variable {str(token.value)} has no assigned register.")

        register = self.register_colors[token.value]
        if register is None:
            # Just return the value held in the Token as a fail safe
            return str(token.value)

        return f"R{register}" # Return the R{some number} register
        

    def _get_op_code(self, operator: Token) -> str:
        '''
        Gets the op-code for the given operator from a three-address-instruction.

        :param operator: The operator we need to get the op-code for
        :type operator: Token
        :return: The string representing the op-code
        :rtype: str
        '''

        return self.opcodes[operator.value]
                
    def _generate_instruction_asm(self, instruction: Instruction) -> list[ASMInstruction]:
        '''
        Generates the assembly code for 1 instruction in the instruction buffer.
        Probably going to be calling this function in some sort of loop.

        :param instruction: The instruction to generate asm code for
        :type instruction: Instruction
        :return: The list of strings containing assembly code for the instruction
        :rtype: list[str]
        '''

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
                    # Negation
                    operation1 = ASMInstruction("MOV", source, dest)
                    operation2 = ASMInstruction("MUL", "#-1", dest)

                    return [operation1, operation2]
                # Not sure what other cases go here as anything like a += 1 would be treated
                # as binary operator and I'm not sure if that is even being supported

                return [ASMInstruction("MOV", source, dest)]
                
            case 2: # Assignment
                # In this case the operator will always be a MOV
                dest = self._get_reg_or_value(instruction.dest)
                source = self._get_reg_or_value(instruction.operand1)
                return [ASMInstruction("MOV", source, dest)]
            
            case _:
                return []
    
    def _output_to_file(self) -> None:
        '''
        Writes the generated assembly instructions to a file in the directory this file is in
        (/imperative/generator)
        '''
        with open("./generator/assembly.txt", "w") as f:
            for instruction in self.generated_asm:
                instruction_str = instruction.op_code + " " + instruction.op1 + "," + instruction.op2
                f.write(f"{instruction_str}\n")

    def generate_assembly(self) -> list[ASMInstruction]:
        '''
        Generates the assembly for every instruction contained within the instruction buffer.
        Returns the assembly as a list but also writes the assembly to an output file
        :return: The list of assembly instructions.
        :rtype: list[str]
        '''
        for instruction in self.buffer.instructions:
            next_instructions: list[ASMInstruction] = self._generate_instruction_asm(instruction)
            self.generated_asm.extend(next_instructions)

        self._output_to_file()

        return self.generated_asm
    