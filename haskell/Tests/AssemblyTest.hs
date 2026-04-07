module Tests.AssemblyTest where

import Output.Assembly

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name 

testAssembly :: IO()
testAssembly = mapM_ putStrLn results

results :: [String]
results = 
    [
        -- Show OpCode
        check "Show OpCode - ADD" (show ADD == "ADD"),
        check "Show OpCode - SUB" (show SUB == "SUB"),
        check "Show OpCode - MUL" (show MUL == "MUL"),
        check "Show OpCode - DIV" (show DIV == "DIV"),
        check "Show OpCode - MOV" (show MOV == "MOV"),

        -- Eq OpCode
        check "Eq OpCode - Equal OpCode" (ADD == ADD),
        check "Eq OpCode - Unequal OpCode" (ADD /= MUL),

        -- Show AssemblyInstruction
        check "Show AssemblyInstruction - ADD instruction" (show (AssemblyInstruction ADD "#1" "R0") == "ADD #1,R0"),
        check "Show AssemblyInstruction - SUB instruction" (show (AssemblyInstruction SUB "#1" "R0") == "SUB #1,R0"),
        check "Show AssemblyInstruction - MUL instruction" (show (AssemblyInstruction MUL "#2" "R0") == "MUL #2,R0"),
        check "Show AssemblyInstruction - DIV instruction" (show (AssemblyInstruction DIV "#2" "R0") == "DIV #2,R0"),
        check "Show AssemblyInstruction - MOV instruction" (show (AssemblyInstruction MOV "#1" "R0") == "MOV #1,R0"),

        -- Eq AssemblyInstruction
        check "Eq AssemblyInstruction - Equal instruction" (AssemblyInstruction MOV "#2" "R0" == AssemblyInstruction MOV "#2" "R0"),
        check "Eq AssemblyInstruction - Unequal instruction" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction ADD "x" "R0"),

        -- Show Assembly
        check "Show Assembly - Multiple instructions" (show (Assembly [AssemblyInstruction MOV "x" "R0", AssemblyInstruction ADD "#1" "R0"]) == "Assembly Instructions: \nMOV x,R0\nADD #1,R0\n")
    ]
