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