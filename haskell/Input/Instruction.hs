module Instruction (Instruction(..),
                          InstructionType(..),
                          getVariables) 
where
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
    | AssignmentIns InstructionType Dest Operand
    deriving (Show, Eq)

-- Public: Retrieves all variable tokens stored in the given instruction
getVariables :: Instruction -> [Token]
getVariables (BinaryIns _ dest op1 _ op2) = filter isVariable [dest, op1, op2]
getVariables (UnaryIns _ dest _ op) = filter isVariable [dest, op]
getVariable (AssignmentIns _ dest op) = filter isVariable [dest, op]

-- Private: Helper that checks if Token is a variable
isVariable :: Token -> Bool
isVariable (Token _ Variable) = True
isVariable _ = False