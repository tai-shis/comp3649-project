import Token

data InstructionType 
    = Invalid
    | BinaryOperator
    | UnaryOperator
    | Assignment
    deriving (Show, Eq)

data Dest = Token
data Operand = Token
data Operator = Token

data Instruction 
    = BinaryIns InstructionType Dest Operand Operator Operand
    | UnaryIns InstructionType Dest Operator Operand
    | AssignmentIns = InstructionType Dest Operand
    deriving (Show, Eq)