class ASMInstruction:
    def __init__(self, op_code: str, op1: str, op2: str):
        '''
        :param op_code: op_code as a single character
        :param op1: source (or register if MOV is being used) operand
        :param op2: destination variable or register
        '''

        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return f"{self.op_code} {self.op1},{self.op2}"