module Tests.InstructionTest where

import Input.Token
import Input.Instruction

-- simple wrapper to keep outputs consistent
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- setting up some dummy tokens for testing
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

-- dummy instructions using the tokens above
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
        -- making sure creation logic works
        check "build binary instruction" (binaryIns == createInstruction (destToken, varTokenA, addOpToken, varTokenB)),
        check "build unary instruction" (unaryIns == createInstruction (destToken, negOpToken, varTokenA)),
        check "build assignment instruction" (assignIns == createInstruction (destToken, litToken)),
        
        -- checking how they print to string
        check "show prints binary correctly" (show binaryIns == "Binary Instruction: x : Destination = a : Variable + : Operator b : Variable"),
        check "show prints unary correctly" (show unaryIns == "Unary Instruction: x : Destination = - : Operator a : Variable"),
        check "show prints assignment correctly" (show assignIns == "Assignment Instruction: x : Destination = 19 : Literal"),

        -- equality checks
        check "instruction equals itself" (binaryIns == binaryIns),
        check "different instructions don't equal" (binaryIns /= assignIns),
        
        -- pulling the destination out
        check "get destination from binary" (getDestination binaryIns == destToken),
        check "get destination from unary" (getDestination unaryIns == destToken),
        check "get destination from assignment" (getDestination assignIns == destToken),
        
        -- variable extraction (ignoring literals/ops)
        check "extract vars from binary" 
            (getVariables (createInstruction (destToken, varTokenA, addOpToken, varTokenB)) 
            == [varTokenA, varTokenB]),
        check "extract vars from binary with literals (returns empty)" 
            (getVariables (createInstruction (destToken, litToken, addOpToken, createToken "1" Literal))
            == []),
        check "extract vars from mixed binary"
            (getVariables (createInstruction (destToken, varTokenA, addOpToken, litToken))
            == [varTokenA]),

        check "extract var from unary"
            (getVariables (createInstruction (destToken, negOpToken, varTokenA))
            == [varTokenA]),
        check "extract var from unary literal (returns empty)"
            (getVariables (createInstruction (destToken, negOpToken, litToken))
            == []),

        check "extract var from assignment"
            (getVariables (createInstruction (destToken, varTokenA))
            == [varTokenA]),
        check "extract var from literal assignment (returns empty)"
            (getVariables (createInstruction (destToken, litToken))
            == []),

        -- testing the big instruction container
        check "empty wrapper has no instructions"
            (getInstructions emptyInstructions == []),
        check "empty wrapper has no live vars"
            (getLiveVariables emptyInstructions == []),

        check "wrapper stores instructions"
            (getInstructions (fromArraysInstructions [assignIns] []) == [assignIns]),
        check "wrapper stores live vars"
            (getLiveVariables (fromArraysInstructions [] ["a", "b"]) == ["a", "b"]),
        check "wrapper stores both at once"
            (getInstructions (fromArraysInstructions [assignIns] ["a"]) == [assignIns]
            && getLiveVariables (fromArraysInstructions [assignIns] ["a"]) == ["a"]),

        -- fetching from populated containers
        check "fetch from populated instructions list"
            (getInstructions (fromArraysInstructions [assignIns, binaryIns] []) == [assignIns, binaryIns]),
        check "fetch from populated live list"
            (getLiveVariables (fromArraysInstructions [] ["a", "b"]) == ["a", "b"]),

        -- printing the big container
        check "print empty instruction list" (showInstructions [] == "Instructions: \n"),
        check "print single instruction list"
            (showInstructions [assignIns]
            == "Instructions: \nAssignment Instruction: x : Destination = 19 : Literal\n"),
        check "print multi instruction list"
            (showInstructions [assignIns, assignIns]
            == "Instructions: \nAssignment Instruction: x : Destination = 19 : Literal\nAssignment Instruction: x : Destination = 19 : Literal\n"),
            
        -- printing live variables
        check "print empty live list" (showLiveVars [] == "Live: "),
        check "print single live var" (showLiveVars ["x"] == "Live: \"x\""),
        check "print multiple live vars" (showLiveVars ["x", "y"] == "Live: \"x\", \"y\""),

        -- full container show instance
        check "show full container matches parts combined"
            (show (fromArraysInstructions [assignIns] ["x"])
            == showInstructions [assignIns] ++ showLiveVars ["x"])
    ]