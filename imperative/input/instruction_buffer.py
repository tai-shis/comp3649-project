from llist import dllist, dllistnode
from instruction import Instruction
            
class InstructionBuffer:
    def __init__(self):
        self.instructions: dllist = dllist()
        self.live_objects: dllist = dllist()

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

if __name__ == "__main__":
    ins = Instruction("d", "g")
    print(ins)
    print("bruh")