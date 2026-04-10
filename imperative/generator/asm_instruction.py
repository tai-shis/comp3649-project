class ASMInstruction:
    def __init__(self, op_code: str, op1: str, op2: str):
        """
        :param op_code: The operation code (e.g. MOV, ADD).
        :param op1: Source operand.
        :param op2: Destination register or variable.
        """

        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2