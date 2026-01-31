from llist import dllist, dllistnode
from input.scanner import Token
            
class Instruction:
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

class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist = dllist() # Instruction objects
        self.live_objects: dllist = dllist() # Strings representing live objects

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
        return [str(node.value) for node in self.instructions.iternodes()]

    def list_live_objects(self) -> list[str]:
        """
            Lists all live objects in the instruction buffer.
            
            :return: A list of all live objects.
            :rtype: list[str]
        """

        return [str(node.value) for node in self.live_objects.iternodes()]

    def __str__(self):
        string = ""

        for node in self.list_instructions():
            string += node + "\n"


        string += "live: "

        for node in self.list_live_objects():
            string += node + ", "

        return string