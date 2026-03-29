module Instruction (Instruction, Instructions, getVariables) where

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
    deriving (Eq)

instance Show Instruction where
    show (BinaryIns _ dest op1 operator op2) = "Binary Instruction: " ++ show dest ++ " = " ++ show op1 ++ " " ++ show operator ++ " " ++ show op2
    show (UnaryIns _ dest operator op) = "Unary Instruction: " ++ show dest ++ " = " ++ show operator ++ " " ++ show op
    show (AssignmentIns _ dest op) = "Assignment Instruction: " ++ show dest ++ " = " ++ show op

instance Show [Instruction] where
    show instructions = "Instructions: \n" ++ map (\x -> show x ++ "\n") instructions

data LiveVariable = Live String

instance Show LiveVariable where
    show (Live var) = var ++ ","

instance Show [LiveVariable] where
    show liveVars = "Live: " ++ map show liveVars

-- Doesn't have to be a pair
data Instructions
    = Instruction ([Instruction],[LiveVariable])

instance Show Instructions where
    show (Instruction (ins,live)) = show ins ++ show live

-- Public: Retrieves all variable tokens stored in the given instruction
getVariables :: Instruction -> [Token]
getVariables (BinaryIns _ dest op1 _ op2) = filter isVariable [dest, op1, op2]
getVariables (UnaryIns _ dest _ op) = filter isVariable [dest, op]
getVariables (AssignmentIns _ dest op) = filter isVariable [dest, op]

-- Private: Helper that checks if Token is a variable
isVariable :: Token -> Bool
isVariable (Token _ Variable) = True
isVariable _ = False