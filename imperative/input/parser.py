from instruction import Instruction
from instruction_buffer import InstructionBuffer
from scanner import Scanner, Token

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def validate_instruction(self, instruction: list[Token]) -> int:
        """
            Validates if the given list of tokens form a valid instruction.

            Parameters:
                instruction (list[Token]): The list of tokens forming an instruction.

            Returns:
                int: 
                    -1 if invalid,
                    0 if binary operator,
                    1 if unary operator,
                    2 if assignment
        """
        match len(instruction):
            case 6: # binary operator check
                if (instruction[0].type == 0 and  # identifier
                    instruction[1].type == 4 and  # equals sign
                    instruction[2].type in [0, 1] and  # identifier or number
                    instruction[3].type == 3 and  # operator
                    instruction[4].type in [0, 1] and  # identifier or number
                    instruction[5].type == 7):  # newline
                    return 0
                else:
                    return -1
            case 5: # unary operator check
                if (instruction[0].type == 0 and  # identifier
                    instruction[1].type == 4 and  # equals sign
                    instruction[2].type == 3 and  # operator
                    instruction[3].type in [0, 1] and  # identifier or number
                    instruction[4].type == 7):  # newline
                    return 1
                else:
                    return -1
            case 4: # assignment check
                if (instruction[0].type == 0 and  # identifier
                    instruction[1].type == 4 and  # equals sign
                    instruction[2].type in [0, 1] and  # identifier or number
                    instruction[3].type == 7):  # newline
                    return 2
                else:
                    return -1
            case _: # invalid instruction length
                return -1
       

    def parse(self) -> InstructionBuffer:
        """
            Parses through tokens provided by the input buffer and constructs
            a list of valid instructions.
        
            Returns:
                InstructionBuffer: The parsed instructions.

            Should be wrapped in a try/catch block.
        """
        instructions: InstructionBuffer = InstructionBuffer()

        token: Token = self.scanner.next_token()
        line: list[Token] = [] # Could change into a different implementation

        # for now parse back into lines ig :/
        while token.type != -1:  # While not EOF
            if token.type != 7: # newline (this isnt magic numbers i promise, its just how i would do it in haskell)
                line.append(token)
            else: 
                line.append(token)
                type: int = self.validate_instruction(line)

                match type:
                    case 0: # binary operator
                        instr = Instruction(
                            type=0,
                            dest=line[0].value,
                            operand1=line[2].value,
                            operator=line[3].value,
                            operand2=line[4].value
                        )
                        instructions.add_instruction(instr)
                    case 1: # unary operator
                        instr = Instruction(
                            type=1,
                            dest=line[0].value,
                            operator=line[2].value,
                            operand2=line[3].value
                        )
                        instructions.add_instruction(instr)
                    case 2: # assignment
                        instr = Instruction(
                            type=2,
                            dest=line[0].value,
                            operand1=line[2].value
                        )
                        instructions.add_instruction(instr)
                    case -1:
                        raise ValueError("Invalid instruction format.")

                line = [] # reset line after validating
                