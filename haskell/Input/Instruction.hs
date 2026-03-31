module Input.Instruction (
    Instructable(createInstruction),
    Instruction,
    Instructions,
    getVariables,
    getInstructions,
    getLiveVariables,
    showInstructions,
    showLiveVars,
    emptyInstructions,
    fromArraysInstructions
) where

import Input.Token
import Lib.Helper (commaSperatedList)

type Dest = Token
type Operand = Token
type Operator = Token
type LiveVariable = String

type BinaryProps = (Dest, Operand, Operator, Operand)
type UnaryProps = (Dest, Operator, Operand)
type AssignmentProps = (Dest, Operand)

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

-- Doesn't have to be a pair

data Instructions = Inst ([Instruction],[LiveVariable])

instance Show Instruction where
    show (BinaryIns _ dest op1 operator op2) = "Binary Instruction: " ++ show dest ++ " = " ++ show op1 ++ " " ++ show operator ++ " " ++ show op2
    show (UnaryIns _ dest operator op) = "Unary Instruction: " ++ show dest ++ " = " ++ show operator ++ " " ++ show op
    show (AssignmentIns _ dest op) = "Assignment Instruction: " ++ show dest ++ " = " ++ show op

instance Show Instructions where
    show (Inst (ins,live)) = showInstructions ins ++ showLiveVars live

class Instructable a where
    createInstruction :: a -> Instruction
instance Instructable BinaryProps where
    createInstruction (dest, op1, operator, op2) = BinaryIns BinaryOperator dest op1 operator op2
instance Instructable UnaryProps where
    createInstruction (dest, operator, op) = UnaryIns UnaryOperator dest operator op
instance Instructable AssignmentProps where
    createInstruction (dest, op) = AssignmentIns Assignment dest op

-- Public: Creates an empty Instructions object
emptyInstructions :: Instructions
emptyInstructions = Inst ([],[])

-- Public: Creates an Instructions object with a list of Instruction objects and Live Variables
fromArraysInstructions :: [Instruction] -> [LiveVariable] -> Instructions
fromArraysInstructions instructions lives = Inst (instructions,lives) 

-- Public: Prints all instructions
showInstructions :: [Instruction] -> String
showInstructions instructions = "Instructions: \n" ++ concatMap (\x -> show x ++ "\n") instructions

-- Public: Prints all live variables
showLiveVars :: [LiveVariable] -> String
showLiveVars liveVars =  "Live: " ++ commaSperatedList liveVars

-- Public: Retrieves all live variables stored in the given Instructions object
getLiveVariables :: Instructions -> [LiveVariable]
getLiveVariables (Inst (_, live)) = live

-- Public: Retrieves all instructions stored in the given Instructions object
getInstructions :: Instructions -> [Instruction]
getInstructions (Inst (instructions, _)) = instructions

-- Public: Retrieves all variable tokens stored in the given instruction
getVariables :: Instruction -> [Token]
getVariables (BinaryIns _ dest op1 _ op2) = filter isVariable [dest, op1, op2]
getVariables (UnaryIns _ dest _ op) = filter isVariable [dest, op]
getVariables (AssignmentIns _ dest op) = filter isVariable [dest, op]

-- Private: Helper that checks if Token is a variable
isVariable :: Token -> Bool
isVariable token = getType token == Variable