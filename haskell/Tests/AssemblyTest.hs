module Tests.AssemblyTest where

import Output.Assembly
import Output.AssemblyGenerator (generateAssembly)
import Input.Token (Token(Tn), TokenType(..))
import Input.Instruction (Instruction(..), InstructionType(..))

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name 

main :: IO()
main = mapM_ putStrLn results

-- using this mock map to test redundancy and register swaps
mockRegMap :: [(String, Int)]
mockRegMap = [("a", 0), ("b", 1), ("c", 2), ("d", 3), ("t1", 0), ("t2", 1)] 

results :: [String]
results = 
    [
        -- checking basic data types and show instances
        check "show ADD" (show ADD == "ADD"),
        check "show SUB" (show SUB == "SUB"),
        check "show MUL" (show MUL == "MUL"),
        check "show DIV" (show DIV == "DIV"),
        check "show MOV" (show MOV == "MOV"),

        check "ADD equals ADD" (ADD == ADD),
        check "SUB equals SUB" (SUB == SUB),
        check "ADD is not SUB" (ADD /= SUB),
        check "MUL is not DIV" (MUL /= DIV),
        check "MOV is not ADD" (MOV /= ADD),

        check "show ADD instruction" (show (AssemblyInstruction ADD "#1" "R0") == "ADD #1,R0"),
        check "show SUB instruction" (show (AssemblyInstruction SUB "R1" "R2") == "SUB R1,R2"),
        check "show MUL instruction" (show (AssemblyInstruction MUL "#10" "R3") == "MUL #10,R3"),
        check "show DIV instruction" (show (AssemblyInstruction DIV "R0" "R1") == "DIV R0,R1"),
        check "show MOV instruction" (show (AssemblyInstruction MOV "x" "R0") == "MOV x,R0"),

        check "instruction equals itself" (AssemblyInstruction MOV "#2" "R0" == AssemblyInstruction MOV "#2" "R0"),
        check "different opcodes aren't equal" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction ADD "#2" "R0"),
        check "different sources aren't equal" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction MOV "#3" "R0"),
        check "different destinations aren't equal" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction MOV "#2" "R1"),

        check "printing multiple instructions" (show (Assembly [AssemblyInstruction MOV "x" "R0", AssemblyInstruction ADD "#1" "R0"]) == "MOV x,R0\nADD #1,R0\n"),

        -- testing the actual assembly generation logic (liveness, math, optimizations)
        check "generate liveness loads and stores" 
            (let (Assembly asm) = generateAssembly [] ["a", "b"] ["c", "d"] mockRegMap 
             in asm == [AssemblyInstruction MOV "a" "R0", AssemblyInstruction MOV "b" "R1", AssemblyInstruction MOV "R2" "c", AssemblyInstruction MOV "R3" "d"]),
            
        check "ignore variables with no register" 
            (let (Assembly asm) = generateAssembly [] ["x", "y"] ["z"] mockRegMap 
             in asm == []),

        check "mixed mapped and unmapped liveness vars" 
            (let (Assembly asm) = generateAssembly [] ["a", "x"] ["y", "b"] mockRegMap 
             in asm == [AssemblyInstruction MOV "a" "R0", AssemblyInstruction MOV "R1" "b"]),

        check "add two variables" 
            (let ins = BinaryIns BinaryOperator (Tn "d" Destination) (Tn "a" Variable) (Tn "+" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R3", AssemblyInstruction ADD "R1" "R3"]),
             
        check "add commutative optimization (skip mov)" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "+" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction ADD "R1" "R0"]),

        check "add two literals" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "5" Literal) (Tn "+" Operator) (Tn "10" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#5" "R0", AssemblyInstruction ADD "#10" "R0"]),

        check "subtract two variables" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "-" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction SUB "R1" "R2"]),
             
        check "subtract literal from variable" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "-" Operator) (Tn "5" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction SUB "#5" "R2"]),
             
        check "subtraction order matters (don't swap!)" 
            -- subtraction isn't commutative, so a = b - a shouldn't swap
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R1" "R0", AssemblyInstruction SUB "R0" "R0"]),

        check "multiply variable and literal" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "*" Operator) (Tn "10" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction MUL "#10" "R2"]),

        check "multiply commutative swap" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "10" Literal) (Tn "*" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MUL "#10" "R0"]),

        check "divide two variables" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "/" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction DIV "R1" "R2"]),

        check "divide literal by variable" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "100" Literal) (Tn "/" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#100" "R2", AssemblyInstruction DIV "R1" "R2"]),

        check "unary minus variable" 
            (let ins = UnaryIns UnaryOperator (Tn "b" Destination) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R1", AssemblyInstruction MUL "#-1" "R1"]),
             
        check "unary minus sharing register" 
            -- t1 and a share R0, skips the MOV
            (let ins = UnaryIns UnaryOperator (Tn "t1" Destination) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MUL "#-1" "R0"]),

        check "unary minus literal" 
            (let ins = UnaryIns UnaryOperator (Tn "a" Destination) (Tn "-" Operator) (Tn "5" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#5" "R0", AssemblyInstruction MUL "#-1" "R0"]),

        check "assign a literal" 
            (let ins = AssignmentIns Assignment (Tn "a" Destination) (Tn "4" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#4" "R0"]),

        check "assign a variable" 
            (let ins = AssignmentIns Assignment (Tn "b" Destination) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R1"]),

        check "redundant assignment check (skip mov)" 
            (let ins = AssignmentIns Assignment (Tn "t1" Destination) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [])
    ]