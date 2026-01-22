class Instruction:
    def __init__(self, dest: str, operand1: str=None, operator: str=None, operand2: str=None):
        if operand1 and operator and operand2:
            self.type = "binary_operator"     
        elif not operand1 and operator and operand2:
            self.type = "unary_operator"
        elif operand1 and not operator and not operand2:
            self.type = "assignment"
        else:
            raise ValueError("Invalid instruction format")

        self.dest = dest
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

    def __str__(self):
        match self.type:
            case "binary_operator":
                return f"{self.dest} = {self.operand1} {self.operator} {self.operand2}"
            case "unary_operator":
                return f"{self.dest} = {self.operator}{self.operand2}"
            case "assignment":
                return f"{self.dest} = {self.operand1}"