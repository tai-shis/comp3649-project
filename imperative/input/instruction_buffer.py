from llist import dllist, dllistnode
from instruction import Instruction
            
class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist[Instruction] = dllist()
        self.live_objects: dllist[str] = dllist()

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def add_live_object(self, live_object: str):
        self.live_objects.append(live_object)

    def list_instructions(self):
        return [str(node.value) for node in self.instructions.iternodes()]

    def list_live_objects(self):
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