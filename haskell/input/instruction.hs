import Token

type Dest = Token
type Operand = Token
type Operator = Token

data InstructionType 
    = Invalid
    | BinaryOperator
    | UnaryOperator
    | Assignment
    deriving (Show, Eq)

data Instruction 
    = BinaryIns InstructionType Dest Operand Operator Operand
    | UnaryIns InstructionType Dest Operator Operand
    | AssignmentIns = InstructionType Dest Operand
    deriving (Show, Eq)

getInstructionDest :: Instruction -> Token
getInstructionDest (Instruction _ dest _ _ _) = dest

getInstructionOperand :: Int -> Instruction -> Token
getInstructionOperand operandNum (Instruction type _ op1 _ op2) = 
    case type of
        BinaryOperator ->
            if (operandNum == 1)
                op1
            else
                op2
        UnaryOperator -> op2
        Assignment -> op1

-- Retrieves all variable tokens stored in the given instruction
getListVariables :: Instruction -> [Token]
getListVariables instruction = 
    [getInstructionDest instruction,
    getInstructionOperand (1 instruction),
    getInstructionOperand (2 instruction)]
