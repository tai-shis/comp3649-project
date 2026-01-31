from input.instruction_buffer import InstructionBuffer, Instruction
from input.scanner import Scanner, Token

class Parser:
    types = {
        'destination': 0,  # ex. 'd', 't3', 'z', destination (variable)
        'variable': 1,     # ex. 'a', 't1', 'b', variables
        'literal': 2,      # ex. '1', '23', '415', any integer literal
        'operator': 3,     # '+', '-', '*', '/' operators
        'equals': 4,       # '=' occurs once
        'live': 5,         # 'live:' occurs once
        'live_symbol': 6,  # ex. 'a,', 'c,', 'd,', etc... (excluding commas in tokens)
        'newline': 7,      # '\n', terminating character
        'EOF': -1          # End of File
    }

    instruction_types = {
        "invalid": -1,
        "binary_operator": 0,
        "unary_operator": 1,
        "assignment": 2
    }

    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.occurred_variables: set[str] = set()

    def _validate_instruction(self, instruction: list[Token]) -> int:
        """
            Validates if the given list of tokens form a valid instruction.

            :param instruction: The list of tokens forming an instruction.
            :type instruction: list[Token]

            :return: The type of instruction:
                    -1 if invalid,
                    0 if binary operator,
                    1 if unary operator,
                    2 if assignment
            :rtype: int
                    
        """
        match len(instruction):
            case 6: # binary operator check
                if (instruction[0].type == self.types["destination"] and  # destination
                    instruction[1].type == self.types["equals"] and  # equals sign
                    instruction[2].type in [self.types["literal"], self.types["variable"]] and  # identifier or number
                    instruction[3].type == self.types["operator"] and  # operator
                    instruction[4].type in [self.types["literal"], self.types["variable"]] and  # identifier or number
                    instruction[5].type == self.types["newline"]):  # newline
                    return self.instruction_types["binary_operator"]                    
            case 5: # unary operator check
                if (instruction[0].type == self.types["destination"] and  # destination
                    instruction[1].type == self.types["equals"] and  # equals sign
                    instruction[2].type == self.types["operator"] and  # operator
                    instruction[3].type in [self.types["literal"], self.types["variable"]] and  # identifier or number
                    instruction[4].type == self.types["newline"]):  # newline
                    return self.instruction_types["unary_operator"]
            case 4: # assignment check
                if (instruction[0].type == self.types["destination"] and  # destination
                    instruction[1].type == self.types["equals"] and  # equals sign
                    instruction[2].type in [self.types["literal"], self.types["variable"]] and  # identifier or number
                    instruction[3].type == self.types["newline"]):  # newline
                    return self.instruction_types["assignment"]
                
        # invalid instruction length or format
        return self.instruction_types["invalid"]
       

    def _parse_instructions(self, instruction_buffer: InstructionBuffer) -> bool:
        """
            Parses through tokens representing instructions, validating
            and adding them to the instruction buffer.
        
            :param instruction_buffer: The instruction buffer to which instructions will be added.
            :type instruction_buffer: InstructionBuffer
            :return: True if EOF is reached, False if 'live:' is encountered.
            :rtype: bool
            :raises ValueError: If an invalid instruction format is encountered.
        """
        token: Token = self.scanner.next_token()
        line: list[Token] = [] # Could change into a different implementation

        # for now parse back into lines ig :/
        while token.type != self.types["EOF"] and token.type != self.types["live"]:  # While not live or EOF
            # Keep track of all tokens in the input
            if token.type == self.types["variable"] or token.type == self.types["destination"]:
                self.occurred_variables.add(token.value)

            line.append(token)

            if token.type == self.types["newline"]:
                type: int = self._validate_instruction(line)

                match type:
                    case 0: # binary operator
                        instr = Instruction(
                            type=0,
                            dest=line[0],
                            operand1=line[2],
                            operator=line[3],
                            operand2=line[4]
                        )
                        instruction_buffer.add_instruction(instr)
                    case 1: # unary operator
                        instr = Instruction(
                            type=1,
                            dest=line[0],
                            operator=line[2],
                            operand2=line[3]
                        )
                        instruction_buffer.add_instruction(instr)
                    case 2: # assignment
                        instr = Instruction(
                            type=2,
                            dest=line[0],
                            operand1=line[2]
                        )
                        instruction_buffer.add_instruction(instr)
                    case -1:
                        raise ValueError(f'Invalid instruction format. {" ".join([token.value for token in line])}')

                line = [] # reset line after validating

            token = self.scanner.next_token() # get next token

        return token.type == self.types["EOF"]

    def _parse_live(self, instruction_buffer: InstructionBuffer) -> None:
        """
            Parses through tokens representing live objects and adds them to the instruction buffer.

            If duplicates are passed, they are ignored.

            :param instruction_buffer: The instruction buffer to which live objects will be added.
            :type instruction_buffer: InstructionBuffer
            :raises ValueError: If a live object has not been declared in previous instructions.
        """
        # Here, "live:" has already been read
        token = self.scanner.next_token()

        # Keep track of objects, dropping duplicates
        seen: set[str] = set()

        while token.type != self.types["EOF"]:
            # Make sure all tokens are live symbols!
            if token.type != self.types["live_symbol"]: 
                raise ValueError(f"Invalid live object format. Expected live symbol, got {token.type_string()}.")
            else:
                # Make sure live object was somewhere in the instructions
                if token.value not in self.occurred_variables: 
                    raise ValueError(f"Live object '{token.value}' has not been declared in previous instructions.")
                
                if token.value not in seen:
                    instruction_buffer.add_live_object(token.value)
                    seen.add(token.value)

            token = self.scanner.next_token()

    def parse(self) -> InstructionBuffer:
        """
            Parses through tokens provided by the input buffer and constructs
            a list of valid instructions.
        
            :return: An InstructionBuffer containing all valid instructions and live objects.
            :rtype: InstructionBuffer
        """
        instruction_buffer: InstructionBuffer = InstructionBuffer()

        # Split into two, instructions, then lives objects.
        eof: bool = self._parse_instructions(instruction_buffer)

        if not eof:
            self._parse_live(instruction_buffer)

        return instruction_buffer