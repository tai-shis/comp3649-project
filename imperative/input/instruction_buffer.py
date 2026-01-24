from llist import dllist, dllistnode
from instruction import Instruction
            
class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist = dllist()
        self.live_objects: dllist = dllist()

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def list_instructions(self):
        return self.instructions.iternodes()

    def __str__(self):
        string = ""

        for node in self.instructions.iternodes():
            string += str(node.value) + "\n"


        string += "live: "

        for node in self.live_objects.iternodes():
            string += str(node.value) + ", "

        return string

if __name__ == "__main__":
    list = dllist()
    
    with open("imperative/tests/input1.txt") as file:
        for line in file:
            sp_line = line.strip().split(' ')
            sp_line.append('\n')
            print(sp_line)
            if "live:" in sp_line:
                break
            instr = Instruction(sp_line[0], operand1=sp_line[2], operator=sp_line[3], operand2=sp_line[4])

            list.append(instr)

    print(list)