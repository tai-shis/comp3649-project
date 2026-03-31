module Tests.InstructionTest where

import Input.Token
import Input.Instruction

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- Sample tokens
destToken :: Token
destToken = Token "x" Destination

varTokenA :: Token
varTokenA = Token "a" Variable

varTokenB :: Token
varTokenB = Token "b" Variable

addOpToken :: Token
addOpToken = Token "+" Operator

negOpToken :: Token
negOpToken = Token "-" Operator

litToken :: Token
litToken = Token "42" Literal

-- Sample instructions
binaryIns :: Instruction
binaryIns = BinaryIns BinaryOperator destToken varTokenA addOpToken varTokenB

unaryIns :: Instruction
unaryIns = UnaryIns UnaryOperator destToken negOpToken varTokenA

assignIns :: Instruction
assignIns = AssignmentIns Assignment destToken litToken

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results =
    -- Construction tests
    [ check "BinaryIns construction"
        (binaryIns == BinaryIns BinaryOperator destToken varTokenA addOpToken varTokenB)
    , check "UnaryIns construction"
        (unaryIns == UnaryIns UnaryOperator destToken negOpToken varTokenA)
    , check "AssignmentIns construction"
        (assignIns == AssignmentIns Assignment destToken litToken)

    -- Show Instruction
    , check "Show BinaryIns"
        (show binaryIns
            == "Binary Instruction: Token \"x\" Destination = Token \"a\" Variable Token \"+\" Operator Token \"b\" Variable")
    , check "Show UnaryIns"
        (show unaryIns
            == "Unary Instruction: Token \"x\" Destination = Token \"-\" Operator Token \"a\" Variable")
    , check "Show AssignmentIns"
        (show assignIns
            == "Assignment Instruction: Token \"x\" Destination = Token \"42\" Literal")

    -- Eq Instruction
    , check "Eq Instruction - equal"
        (binaryIns == binaryIns)
    , check "Eq Instruction - unequal"
        (binaryIns /= assignIns)

    -- getVariables on BinaryIns
    , check "getVariables BinaryIns - all variables"
        (getVariables (BinaryIns BinaryOperator (Token "x" Variable) varTokenA addOpToken varTokenB)
            == [Token "x" Variable, varTokenA, varTokenB])
    , check "getVariables BinaryIns - no variables"
        (getVariables (BinaryIns BinaryOperator destToken litToken addOpToken (Token "1" Literal))
            == [])
    , check "getVariables BinaryIns - mixed tokens"
        (getVariables (BinaryIns BinaryOperator destToken varTokenA addOpToken litToken)
            == [varTokenA])

    -- getVariables on UnaryIns
    , check "getVariables UnaryIns - with variable"
        (getVariables (UnaryIns UnaryOperator destToken negOpToken varTokenA)
            == [varTokenA])
    , check "getVariables UnaryIns - no variables"
        (getVariables (UnaryIns UnaryOperator destToken negOpToken litToken)
            == [])

    -- getVariables on AssignmentIns
    , check "getVariables AssignmentIns - with variables"
        (getVariables (AssignmentIns Assignment (Token "x" Variable) varTokenA)
            == [Token "x" Variable, varTokenA])
    , check "getVariables AssignmentIns - no variables"
        (getVariables (AssignmentIns Assignment destToken litToken)
            == [])

    -- showInstructions
    , check "showInstructions - empty list"
        (showInstructions [] == "Instructions: \n")
    , check "showInstructions - single instruction"
        (showInstructions [assignIns]
            == "Instructions: \nAssignment Instruction: Token \"x\" Destination = Token \"42\" Literal\n")
    , check "showInstructions - multiple instructions"
        (showInstructions [assignIns, AssignmentIns Assignment (Token "y" Destination) (Token "1" Literal)]
            == "Instructions: \nAssignment Instruction: Token \"x\" Destination = Token \"42\" Literal\nAssignment Instruction: Token \"y\" Destination = Token \"1\" Literal\n")

    -- showLiveVars
    , check "showLiveVars - empty list"
        (showLiveVars [] == "Live: ")
    , check "showLiveVars - single variable"
        (showLiveVars [LiveVar "x"] == "Live: x,")
    , check "showLiveVars - multiple variables"
        (showLiveVars [LiveVar "x", LiveVar "y"] == "Live: x,y,")

    -- Show Instructions (uses the Instruction constructor from data Instructions)
    , check "Show Instructions"
    (show (Instructions ([assignIns], [LiveVar "x"]))
        == showInstructions [assignIns] ++ showLiveVars [LiveVar "x"])
    ]