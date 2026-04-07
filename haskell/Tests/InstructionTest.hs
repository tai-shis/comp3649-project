module Tests.InstructionTest where

import Input.Token
import Input.Instruction

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- Sample tokens
destToken :: Token
destToken = createToken "x" Destination

varTokenA :: Token
varTokenA = createToken "a" Variable

varTokenB :: Token
varTokenB = createToken "b" Variable

addOpToken :: Token
addOpToken = createToken "+" Operator

negOpToken :: Token
negOpToken = createToken "-" Operator

litToken :: Token
litToken = createToken "19" Literal

-- Sample instructions
binaryIns :: Instruction
binaryIns = createInstruction (destToken, varTokenA, addOpToken, varTokenB)

unaryIns :: Instruction
unaryIns = createInstruction (destToken, negOpToken, varTokenA)

assignIns :: Instruction
assignIns = createInstruction (destToken, litToken)

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results =
    [
        -- createInstruction
        check "createInstuction - BinaryProps" (binaryIns == createInstruction (destToken, varTokenA, addOpToken, varTokenB)),
        check "createInstuction - UnaryProps" (unaryIns == createInstruction (destToken, negOpToken, varTokenA)),
        check "createInstuction - AssignmentProps" (assignIns == createInstruction (destToken, litToken)),
        
        -- Show Instruction
        check "Show Binary Instruction" (show binaryIns == "Binary Instruction: x : Destination = a : Variable + : Operator b : Variable"),
        check "Show Unary Instruction" (show unaryIns == "Unary Instruction: x : Destination = - : Operator a : Variable"),
        check "Show Assignment Instruction" (show assignIns == "Assignment Instruction: x : Destination = 19 : Literal"),

        -- Eq Instruction
        check "Eq Instruction - equal" (binaryIns == binaryIns),
        check "Eq Instruction - unequal" (binaryIns /= assignIns),
        
        -- getDestination
        check "getDestination - BinaryIns" (getDestination binaryIns == destToken),
        check "getDestination - UnaryIns" (getDestination unaryIns == destToken),
        check "getDestination - AssignIns" (getDestination assignIns == destToken),
        
        -- getVariables on BinaryIns
        check "getVariables - BinaryIns" 
            (getVariables (createInstruction (destToken, varTokenA, addOpToken, varTokenB)) 
            == [varTokenA, varTokenB]),
        check "getVariables BinaryIns - no variables" 
            (getVariables (createInstruction (destToken, litToken, addOpToken, createToken "1" Literal))
            == []),
        check "getVariables BinaryIns - mixed tokens"
            (getVariables (createInstruction (destToken, varTokenA, addOpToken, litToken))
            == [varTokenA]),

        -- getVariables on UnaryIns
        check "getVariables UnaryIns - variable operand"
            (getVariables (createInstruction (destToken, negOpToken, varTokenA))
            == [varTokenA]),
        check "getVariables UnaryIns - no variables"
            (getVariables (createInstruction (destToken, negOpToken, litToken))
            == []),

        -- getVariables on AssignmentIns
        check "getVariables AssignmentIns - variable operand"
            (getVariables (createInstruction (destToken, varTokenA))
            == [varTokenA]),
        check "getVariables AssignmentIns - no variables"
            (getVariables (createInstruction (destToken, litToken))
            == []),

        -- emptyInstruction
        check "emptyInstructions - empty instructions list"
            (getInstructions emptyInstructions == []),
        check "emptyInstructions - empty live variables list"
            (getLiveVariables emptyInstructions == []),

        -- fromArraysInstructions
        check "fromArraysInstructions - stores instructions"
            (getInstructions (fromArraysInstructions [assignIns] []) == [assignIns]),
        check "fromArraysInstructions - stores live variables"
            (getLiveVariables (fromArraysInstructions [] ["a", "b"]) == ["a", "b"]),
        check "fromArraysInstructions - stores both"
        (getInstructions (fromArraysInstructions [assignIns] ["a"]) == [assignIns]
            && getLiveVariables (fromArraysInstructions [assignIns] ["a"]) == ["a"]),

        -- getInstructions
        check "getInstructions - empty" (getInstructions emptyInstructions == []),
        check "getInstructions - populated"
        (getInstructions (fromArraysInstructions [assignIns, binaryIns] []) == [assignIns, binaryIns]),

        -- getLiveVariables
        check "getLiveVariables - empty" (getLiveVariables emptyInstructions == []),
        check "getLiveVariables - populated"
            (getLiveVariables (fromArraysInstructions [] ["a", "b"]) == ["a", "b"]),

        -- showInstructions
        check "showInstructions - empty list" (showInstructions [] == "Instructions: \n"),
        check "showInstructions - single instruction"
            (showInstructions [assignIns]
            == "Instructions: \nAssignment Instruction: x : Destination = 19 : Literal\n"),
        check "showInstructions - multiple instructions"
            (showInstructions [assignIns, assignIns]
            == "Instructions: \nAssignment Instruction: x : Destination = 19 : Literal\nAssignment Instruction: x : Destination = 19 : Literal\n"),
            
        -- showLiveVars
        check "showLiveVars - empty list" (showLiveVars [] == "Live: "),
        check "showLiveVars - single variable" (showLiveVars ["x"] == "Live: \"x\""),
        check "showLiveVars - multiple variables" (showLiveVars ["x", "y"] == "Live: \"x\", \"y\""),

        -- Show Instructions
        check "Show Instructions"
        (show (fromArraysInstructions [assignIns] ["x"])
            == showInstructions [assignIns] ++ showLiveVars ["x"])
    ]