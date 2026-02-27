class ASMInstruction:
    def _init_(self, op_code: str, op1: str, op2: str):
        '''
        :param op_code: op_code as a single character ('+', '-', '*', '/', 'm')
        :param op1: source (or register if MOV is being used) operand
        :param op2: destination variable or register
        '''

        if (len(op_code) > 1):
            ValueError("op_code must only be one character ('+', '-', '*', '/', 'm')")

        self.op_code = self.opcodes[op_code]
        self.op1 = op1
        self.op2 = op2

        self.opcodes = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            'm': 'MOV'
        }
