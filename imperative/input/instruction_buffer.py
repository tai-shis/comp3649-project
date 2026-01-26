from llist import dllist, dllistnode
            
class Instruction:
    def __init__(self, type: int, dest: str, operand1: str=None, operator: str=None, operand2: str=None):
        self.type: int = type
        self.dest: str = dest
        self.operand1: str = operand1
        self.operator: str = operator
        self.operand2: str = operand2

    def __str__(self):
        match self.type:
            case 0:
                return f"{self.dest} = {self.operand1} {self.operator} {self.operand2}"
            case 1:
                return f"{self.dest} = {self.operator}{self.operand2}"
            case 2:
                return f"{self.dest} = {self.operand1}"

class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist = dllist() # Instruction objects
        self.live_objects: dllist = dllist() # strings representing live objects

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

    def list_instructions(self) -> list[str]:
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

# if __name__ == "__main__":
#     list = dllist()
    
#     with open("imperative/tests/input1.txt") as file:
#         for line in file:
#             sp_line = line.strip().split(' ')
#             sp_line.append('\n')
#             print(sp_line)
#             if "live:" in sp_line:
#                 break
#             instr = Instruction(sp_line[0], operand1=sp_line[2], operator=sp_line[3], operand2=sp_line[4])

#             list.append(instr)

#     print(list)