from input.token import Token

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