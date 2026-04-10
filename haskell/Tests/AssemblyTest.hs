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
        check "Show OpCode - ADD" (show ADD == "ADD"),
        check "Show OpCode - SUB" (show SUB == "SUB"),
        check "Show OpCode - MUL" (show MUL == "MUL"),
        check "Show OpCode - DIV" (show DIV == "DIV"),
        check "Show OpCode - MOV" (show MOV == "MOV"),

        check "Eq OpCode - Equal (ADD == ADD)" (ADD == ADD),
        check "Eq OpCode - Equal (SUB == SUB)" (SUB == SUB),
        check "Eq OpCode - Unequal (ADD /= SUB)" (ADD /= SUB),
        check "Eq OpCode - Unequal (MUL /= DIV)" (MUL /= DIV),
        check "Eq OpCode - Unequal (MOV /= ADD)" (MOV /= ADD),

        check "Show AssemblyInst - ADD" (show (AssemblyInstruction ADD "#1" "R0") == "ADD #1,R0"),
        check "Show AssemblyInst - SUB" (show (AssemblyInstruction SUB "R1" "R2") == "SUB R1,R2"),
        check "Show AssemblyInst - MUL" (show (AssemblyInstruction MUL "#10" "R3") == "MUL #10,R3"),
        check "Show AssemblyInst - DIV" (show (AssemblyInstruction DIV "R0" "R1") == "DIV R0,R1"),
        check "Show AssemblyInst - MOV" (show (AssemblyInstruction MOV "x" "R0") == "MOV x,R0"),

        check "Eq AssemblyInst - Same" (AssemblyInstruction MOV "#2" "R0" == AssemblyInstruction MOV "#2" "R0"),
        check "Eq AssemblyInst - Diff OpCode" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction ADD "#2" "R0"),
        check "Eq AssemblyInst - Diff Source" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction MOV "#3" "R0"),
        check "Eq AssemblyInst - Diff Dest" (AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction MOV "#2" "R1"),

        check "Show Assembly - Multi" (show (Assembly [AssemblyInstruction MOV "x" "R0", AssemblyInstruction ADD "#1" "R0"]) == "MOV x,R0\nADD #1,R0\n"),

        -- testing the actual assembly generation logic (liveness, math, optimizations)
        check "Gen: Live Entry/Exit Complete" 
            (let (Assembly asm) = generateAssembly [] ["a", "b"] ["c", "d"] mockRegMap 
             in asm == [AssemblyInstruction MOV "a" "R0", AssemblyInstruction MOV "b" "R1", AssemblyInstruction MOV "R2" "c", AssemblyInstruction MOV "R3" "d"]),
            
        check "Gen: Memory Fallback (Ignore missing registers)" 
            (let (Assembly asm) = generateAssembly [] ["x", "y"] ["z"] mockRegMap 
             in asm == []),

        check "Gen: Mixed Liveness (Some registered, some not)" 
            (let (Assembly asm) = generateAssembly [] ["a", "x"] ["y", "b"] mockRegMap 
             in asm == [AssemblyInstruction MOV "a" "R0", AssemblyInstruction MOV "R1" "b"]),

        check "Gen: ADD (Var + Var) Diff Reg" 
            (let ins = BinaryIns BinaryOperator (Tn "d" Destination) (Tn "a" Variable) (Tn "+" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R3", AssemblyInstruction ADD "R1" "R3"]),
             
        check "Gen: ADD Commutative Swap (Op2 is Dest)" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "+" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction ADD "R1" "R0"]),

        check "Gen: ADD (Lit + Lit)" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "5" Literal) (Tn "+" Operator) (Tn "10" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#5" "R0", AssemblyInstruction ADD "#10" "R0"]),

        check "Gen: SUB (Var - Var)" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "-" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction SUB "R1" "R2"]),
             
        check "Gen: SUB (Var - Lit)" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "-" Operator) (Tn "5" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction SUB "#5" "R2"]),
             
        check "Gen: SUB No Swap (Op2 is Dest)" 
            -- subtraction isn't commutative, so a = b - a shouldn't swap
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R1" "R0", AssemblyInstruction SUB "R0" "R0"]),

        check "Gen: MUL (Var * Lit)" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "*" Operator) (Tn "10" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction MUL "#10" "R2"]),

        check "Gen: MUL Commutative Swap (Op2 is Dest)" 
            (let ins = BinaryIns BinaryOperator (Tn "a" Destination) (Tn "10" Literal) (Tn "*" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MUL "#10" "R0"]),

        check "Gen: DIV (Var / Var)" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "a" Variable) (Tn "/" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R2", AssemblyInstruction DIV "R1" "R2"]),

        check "Gen: DIV (Lit / Var)" 
            (let ins = BinaryIns BinaryOperator (Tn "c" Destination) (Tn "100" Literal) (Tn "/" Operator) (Tn "b" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#100" "R2", AssemblyInstruction DIV "R1" "R2"]),

        check "Gen: Unary (-Var) Diff Reg" 
            (let ins = UnaryIns UnaryOperator (Tn "b" Destination) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R1", AssemblyInstruction MUL "#-1" "R1"]),
             
        check "Gen: Unary (-Var) Same Reg" 
            -- t1 and a share R0, skips the MOV
            (let ins = UnaryIns UnaryOperator (Tn "t1" Destination) (Tn "-" Operator) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MUL "#-1" "R0"]),

        check "Gen: Unary (-Lit)" 
            (let ins = UnaryIns UnaryOperator (Tn "a" Destination) (Tn "-" Operator) (Tn "5" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#5" "R0", AssemblyInstruction MUL "#-1" "R0"]),

        check "Gen: Assign (Dest = Lit)" 
            (let ins = AssignmentIns Assignment (Tn "a" Destination) (Tn "4" Literal)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "#4" "R0"]),

        check "Gen: Assign (Dest = Var) Diff Reg" 
            (let ins = AssignmentIns Assignment (Tn "b" Destination) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [AssemblyInstruction MOV "R0" "R1"]),

        check "Gen: Assign (Dest = Var) Redundancy Check" 
            (let ins = AssignmentIns Assignment (Tn "t1" Destination) (Tn "a" Variable)
                 (Assembly asm) = generateAssembly [ins] [] [] mockRegMap
             in asm == [])
    ]