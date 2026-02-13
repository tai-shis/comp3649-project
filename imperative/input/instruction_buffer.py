from llist import dllist, dllistnode
from input.scanner import Token
            
class Instruction:
    instruction_types = {
        "invalid": -1,
        "binary_operator": 0,
        "unary_operator": 1,
        "assignment": 2
    }

    def __init__(self, type: int, dest: Token, operand1: Token=None, operator: Token=None, operand2: Token=None):
        self.type: int = type
        self.dest: Token = dest
        self.operand1: Token = operand1
        self.operator: Token = operator
        self.operand2: Token = operand2

    def __str__(self):
        match self.type:
            case 0:
                return f"{self.dest.value} = {self.operand1.value} {self.operator.value} {self.operand2.value}"
            case 1:
                return f"{self.dest.value} = {self.operator.value}{self.operand2.value}"
            case 2:
                return f"{self.dest.value} = {self.operand1.value}"
            
    def get_variables(self) -> list[Token]:
        """
        Retrieves all variable tokens involved in this instruction.
        
        :return: A list of variable tokens.
        :rtype: list[Token]
        """

        variable_type = 1 # Token type for variables
        variables: list[Token] = []

        variables.append(self.dest)
        variables.append(self.operand1) if self.operand1 and self.operand1.type == variable_type else None
        variables.append(self.operand2) if self.operand2 and self.operand2.type == variable_type else None

        return variables

class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist = dllist() # Instruction objects
        self.live_objects: dllist = dllist() # Strings representing live objects
        self.occured_variables: set[str] = set() # Set of unique variable names that have occurred in instructions

    def add_instruction(self, instruction: Instruction) -> None:
        """
        Adds an instruction to the instruction buffer.
        
        :param instruction: The instruction to add.
        :type instruction: Instruction
        """
        self.instructions.append(instruction)

    def add_live_object(self, live_object: str) -> None:
        """
        Adds a live object to the instruction buffer.

        :param live_object: The live object to add.
        :type live_object: str
        """
        self.live_objects.append(live_object)

    def list_instructions(self) -> list[Token]:
        """
            Lists all instructions in the instruction buffer.

            :return: A list of string representations of all instructions.
            :rtype: list[str]
        """
        return [node.value for node in self.instructions.iternodes()]

    def list_live_objects(self) -> list[str]:
        """
            Lists all live objects in the instruction buffer.
            
            :return: A list of all live objects.
            :rtype: list[str]
        """

        return [node.value for node in self.live_objects.iternodes()]

    def get_instructions(self) -> dllist:
        """
        Gets the instructions in the instruction buffer.

        :return: The list of instructions.
        :rtype: dllist
        """
        return self.instructions

    def get_live_objects(self) -> dllist:
        """
        Gets the live objects in the instruction buffer.

        :return: The live objects.
        :rtype: dllist
        """
        return self.live_objects
    
    def set_occured_variables(self, variables: set[str]) -> None:
        """
        Sets the occurred variables in the instruction buffer.
        :param variables: The set of occurred variables.
        :type variables: set[str]
        """
        self.occured_variables = variables
    
    def get_occured_variables(self) -> set[str]:
        """
        Gets a set of unique occurred variables in the instruction buffer.
        :return: A set of occurred variables.
        :rtype: set[str]
        """
        return self.occured_variables

    def __str__(self):
        string = ""

        for node in self.list_instructions():
            string += node + "\n"


        string += "live: "

        for node in self.list_live_objects():
            string += node + ", "

        return string
