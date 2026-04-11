import os

from generator.asm_instruction import ASMInstruction
from intermediate.interference_graph import InterferenceGraph
from intermediate.liveness import Liveness
from input.instruction_buffer import InstructionBuffer
from input.instruction import Instruction
from input.token import Token

class ASMGenerator:
    def __init__(self,
                 instruction_buffer: InstructionBuffer,
                 interference_graph: InterferenceGraph,
                 liveness: Liveness):
        self.buffer: InstructionBuffer = instruction_buffer
        self.register_colors: dict[str, int | None] = interference_graph.colors
        self.liveness = liveness # Track liveness so we know when to free registers and perform operations in place

        # This will be formatted like ["MOV a,R0", "ADD #1,R0"] where each string entry can be separated by a "\n" when being printed
        # out to the console of output file
        self.generated_asm: list[ASMInstruction] = []
        self.in_register: set[str] = set() # Track variables currently loaded into registers
        
        self.opcodes = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
        }
    
    def _get_op_code(self, op_token: Token) -> str:
        '''
        Returns the string representation of the operator.
        i.e. op_token.value == '+' -> "ADD"
        '''
        return self.opcodes[op_token.value]

    def _get_reg(self, token: Token) -> str:
        '''
        Gets the appropriate register for the given token.
        If token is a literal, return nothing as a failsafe.
        '''
        if token.value not in self.register_colors:
            raise ValueError(f"Variable: {token.value} does not have a register assigned to it.")
        
        register = self.register_colors[token.value]
        
        if register is None:
            raise ValueError(f"Variable: {token.value} is known but never assigned a register.\nContinuing could cause a register conflict.")
        
        return f"R{register}"

    def _load_variable(self, token: Token) -> list[ASMInstruction]:
        '''
        If variable in the token is not loaded into its register 
        (i.e. MOV var,RX was not done earlier), do it now.
        Will not return anything for a literal 
        '''
        if token.type == 2:
            return []
        
        if token.value not in self.in_register:
            # Now we generate the MOV instruction and add the variable to the "in_register" set
            token_register = self._get_reg(token)
            self.in_register.add(token.value)
            return [ASMInstruction("MOV", token.value, token_register)]

        return []

    def _get_operand_str(self, token: Token) -> str:
        '''
        Gets the operand string for instruction construction.
        Literals will have '#' prepended on them.
        Variables will return as 'RX' where X is some integer. 
        '''
        if token.type == 2:
            return f"#{token.value}"
        return self._get_reg(token)

    def _generate_instruction_asm(self,
                                  instruction: Instruction,
                                  line_liveness: dict[str, int],
                                  next_liveness: dict[str, int]) -> list[ASMInstruction]:
        '''
        Generates the assembly code for the given instruction.

        :param instruction: The instruction to generate asm code for
        :type instruction: Instruction
        :return: The list of strings containing assembly code for the instruction
        :rtype: list[str]
        '''

        asm: list[ASMInstruction] = []

        match instruction.type:
            case 0: # Binary Instruction: x = a + 2 
                
                asm.extend(self._load_variable(instruction.operand1))

                dest_reg = self._get_reg(instruction.dest)
                op1_str = self._get_operand_str(instruction.operand1)
                op2_str = self._get_operand_str(instruction.operand2)
                op_code = self._get_op_code(instruction.operator)

                # If dest and operand1 are equal (i.e. a = a + 1)
                if dest_reg != op1_str:
                    if dest_reg == op2_str and op_code in ('ADD', 'MUL'):
                        # Case: a = b + a, swap since ADD and MUL commute
                        asm.extend(self._load_variable(instruction.operand2))
                        op1_str, op2_str = op2_str, op1_str
                    elif dest_reg == op2_str and op_code in ('SUB', 'DIV'):
                        # Case: a = 1 - a, does not commute so store 'a' to memory
                        asm.extend(self._load_variable(instruction.operand2))
                        asm.append(ASMInstruction("MOV", dest_reg, instruction.operand2.value))
                        asm.append(ASMInstruction("MOV", op1_str, dest_reg))
                        op2_str = instruction.operand2.value
                    else:
                        asm.append(ASMInstruction("MOV", op1_str, dest_reg))
                        asm.extend(self._load_variable(instruction.operand2))
                else:
                    asm.extend(self._load_variable(instruction.operand2))

                asm.append(ASMInstruction(op_code, op2_str, dest_reg))
                self.in_register.add(instruction.dest.value)

            case 1: # Unary Instruction: x = -a
                asm.extend(self._load_variable(instruction.operand2))

                dest_reg = self._get_reg(instruction.dest)
                source_str = self._get_operand_str(instruction.operand2)
                op_symbol = instruction.operator.value

                if op_symbol == '-':
                    if  dest_reg != source_str:
                        asm.append(ASMInstruction("MOV", source_str, dest_reg))
                    asm.append(ASMInstruction("MUL", "#-1", dest_reg))
                else:
                    if dest_reg != source_str:
                        asm.append(ASMInstruction("MOV", source_str, dest_reg))

                self.in_register.add(instruction.dest.value)
                
            case 2: # Assignment: x = a
                # First we need to ensure 'a' is loaded into its register. If not, we will get 'MOV a,Ra' from this.
                asm.extend(self._load_variable(instruction.operand1))

                dest_reg = self._get_reg(instruction.dest)
                source_str = self._get_operand_str(instruction.operand1) # This could be a register (RX) or a literal (#<num>). Can't know for sure

                # Must make sure the source variable is not assigned the same register as the destination. 
                # If not we can complete the move right here.
                if dest_reg != source_str:
                    asm.extend([ASMInstruction("MOV", source_str, dest_reg)])
                
                self.in_register.add(instruction.dest.value)

            case _: # Instruction somehow made it this far while being invalid. TODO: Should we raise error here?
                return []
            
        # --- Store-back functionality --- 
        dest_var = instruction.dest.value
        dest_reg = self._get_reg(instruction.dest)

        # Check all operands to see if any sharing variable is about to use their register
        if instruction.type == 0:
            operands = [instruction.operand1, instruction.operand2]
        elif instruction.type == 1:
            operands = [instruction.operand2]
        elif instruction.type == 2:
            operands = [instruction.operand1]
        else:
            operands = []

        for operand in operands:
            if operand is None or operand.type == 2:  # skip literals
                continue
            operand_var = operand.value
            operand_reg_color = self.register_colors.get(operand_var)
            for var, color in self.register_colors.items():
                if color == operand_reg_color and var != operand_var and next_liveness.get(var, 2) != 2:
                    if operand_var in self.in_register and line_liveness.get(operand_var, 2) == 1:
                
                        asm.extend([ASMInstruction("MOV", f"R{operand_reg_color}", operand_var)])
                        self.in_register.discard(operand_var)
                        break

        return asm

    def _write_live_on_exit(self):
        '''
        Adds the instructions that write the variables live on exit back
        into memory for use in other files.
        '''
        liveness_list = self.liveness.get_liveness()
        last_line = liveness_list[-1]

        for var,state in last_line.items():
            if state == 1: # Live on exit
                register = self.register_colors.get(var)
                if register is not None:
                    self.generated_asm.extend([ASMInstruction("MOV", f"R{register}", var)])

    def _output_to_file(self, output_file: str):
        '''
        Outputs the generated assembly instructions to a file in generated/
        '''
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            for ins in self.generated_asm:
                line = ins.op_code + " " + ins.op1 + "," + ins.op2
                f.write(f"{line}\n")

    def generate_assembly(self, input_file: str) -> list[ASMInstruction]:
        '''
        Generates assembly instructions for every instruction contained win the instruction buffer.
        Output: generated/<input_file>.s
        '''

        liveness_list = self.liveness.get_liveness()

        for i, instruction in enumerate(self.buffer.instructions):
            
            if i < len(liveness_list):
                line_liveness = liveness_list[i]
            else:
                line_liveness = {}
            
            if (i + 1) < len(liveness_list):
                next_liveness = liveness_list[i + 1]
            else:
                next_liveness = {}
            
            new_asm_instruction: list[ASMInstruction] = self._generate_instruction_asm(instruction, line_liveness, next_liveness)
            self.generated_asm.extend(new_asm_instruction)

        self._write_live_on_exit()
        
        self._output_to_file(input_file)

        return self.generated_asm