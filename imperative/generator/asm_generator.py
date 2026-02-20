'''
- Traverse InstructionBuffer to build corressponding assembly language sequence
- Each three-address instruction will corresspond to one or two ASM language instructions.
    - Register assignments from graph colouring will assist in this as well as later optimizations

ASM OpCodes: [ADD src,Ri, SUB src,Ri, MUL src,Ri, DIV src,Ri, MOV src,Ri, MOV Ri,dst]
    - Where Ri is a register 0 <= i < n (n is number of registers available)
    - ADD src,Ri -> adds src operand to the contents of Ri and stores the sum in Ri
    - SUB src,Ri -> subtracts the src operand from the contents of Ri and stores the difference in Ri
    - MUL src,Ri -> multiplies the src operand by the contents of Ri and stores the product in Ri
    - DIV src,Ri -> divides the contents of Ri by the src operand and stores the quotient in Ri
    - MOV src,Ri -> copies the contents of src into Ri
    - MOV Ri,dst -> copies the contents of Ri into dst
There are modes for src:
    - immediate mode: #x -> x is an integer literal
    - absolute mode: x -> x is the name of a variable
    - register direct mode: Ri -> Ri is a register as seen above
There are modes for dst:
    - absolute mode: x -> x is the name of a variable
    - register direct mode: Ri -> Ri is a register as seen above

Example:

Three-address-instructions
    a = a + 1
    t1 = a * 4
    t2 = t1 + 1
    b = t2 - t1

ASM code
    MOV a,R0 ; Allocate a to R0
    ADD #1,R0
    MOV R0,R1 ; Allocate t1 to R1
    MUL #4,R1 
    MOV R1,R2 ; Allocate t2 to R2 
    ADD #1,R2
    MOV R2,R5 ; R5 is allocated to b
    SUB R1,R2 ; Subtract t1 from t2

So if we traverse through the InstructionBuffer with the type="binary_operator", we know we are probably going to have to use MOV at least once,
some arithmetic operator like MUL, ADD, SUB, DIV, and then possibly another MOV.
If we see something like type="assignment", we just going to be using a MOV

This can be deleted anytime really. Just put this here as I started so I don't have to
reference D2L
'''

from intermediate.interference_graph import InterferenceGraph
from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction

class ASMGenerator:
    def __init__(self, instruction_buffer: InstructionBuffer, interference_graph: InterferenceGraph):
        self.buffer = instruction_buffer
        self.register_colors = interference_graph.colors

        self.opcodes = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
        }

        # This will be formatted like ["MOV a,R0", "ADD #1,R0"] where each string entry can be separated by a "\n" when being printed
        # out to the console of output file
        self.generated_asm = []

    def generate_instruction_asm(self, instruction: Instruction) -> list[str]:
        '''
        Generates the assembly code for 1 instruction in the instruction buffer
        and adds it to the generated_asm list. Probably going to be calling this function in
        some sort of loop

        :param instruction: The instruction to generate asm code for
        :type instruction: Instruction
        :return: The list of strings containing assembly code for the instruction
        :rtype: list[str]
        '''

        match instruction.type:
            case 'binary_operator':
                
                dest = self.get_register(instruction.dest)
                op1 = self.get_register(instruction.operand1)
                op2 = self.get_register(instruction.operand2)

                operation1 = f"MOV {op1},{dest}"
                op_code = self.get_op_code(instruction.operator)
                operation2 = f"{op_code} ,{op2}{dest}"

                return [operation1, operation2]

            case 'unary_operator':
                # Example: Assume b is already live and stored in R0
                # x = -b
                # MOV R0, R1 ; Storing x in R1
                # MUL #-1,R1 ; taking inverse of b and storing in x (value in R0)

                dest = self.get_register(instruction.dest)
                source = self.get_register(instruction.operand2)
                op_symbol = instruction.operator.value

                if (op_symbol == '-'):
                    # Negation
                    operation1 = f"MOV {source},{dest}"
                    operation2 = f"MUL #-1,{dest}"

                    return [operation1, operation2]
                # Not sure what other cases go here as anything like a += 1 would be treated
                # as binary operator and I'm not sure if that is even being supported
                


            case 'assignment':
                # In this case the operator will always be a MOV
                op_code = 'MOV'
                dest = self.get_register(instruction.dest)
                source = self.get_operand(instruction.operand1)
                return op_code + ' ' + source + ',' + dest

        # operator = self.get_operator(instruction.operator) # i.e. MUL if instruction is b = a * t1
        # destination = self.get_register(instruction.dest) # i.e. b if instruction is b = a * t1
        # op1 = self.get_register(instruction.operand1) # i.e. R1 if 'a' should be stored in R1 and instruction is b = a * t1
        # op2 = self.get_register(instruction.operand2) # i.e. R0 if 't1' should be stored in R0 and instruction is b = a * t1


