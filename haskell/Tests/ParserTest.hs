module Tests.ParserTest where

import Input.Token (Token(Tn), TokenType(..))
import Input.Instruction (Instruction(..), InstructionType(..), Instructions, getInstructions, getLiveVariables)
import Input.Parser (parse)

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name 

main :: IO()
main = mapM_ putStrLn results

results :: [String]
results = 
    [
        -- testing all the binary operations and permutations
        check "Parse Binary: Var + Var" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "b" Variable, Tn "+" Operator, Tn "c" Variable]]) 
            == [BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "+" Operator) (Tn "c" Variable)]),
            
        check "Parse Binary: Var * Lit" 
            (getInstructions (parse [[Tn "t1" Destination, Tn "=" Equals, Tn "x" Variable, Tn "*" Operator, Tn "4" Literal]]) 
            == [BinaryIns BinaryOperator (Tn "t1" Destination) (Tn "x" Variable) (Tn "*" Operator) (Tn "4" Literal)]),

        check "Parse Binary: Lit / Var" 
            (getInstructions (parse [[Tn "t2" Destination, Tn "=" Equals, Tn "10" Literal, Tn "/" Operator, Tn "y" Variable]]) 
            == [BinaryIns BinaryOperator (Tn "t2" Destination) (Tn "10" Literal) (Tn "/" Operator) (Tn "y" Variable)]),

        check "Parse Binary: Lit - Lit" 
            (getInstructions (parse [[Tn "res" Destination, Tn "=" Equals, Tn "100" Literal, Tn "-" Operator, Tn "50" Literal]]) 
            == [BinaryIns BinaryOperator (Tn "res" Destination) (Tn "100" Literal) (Tn "-" Operator) (Tn "50" Literal)]),

        -- unary and assignment stuff
        check "Parse Unary: Negation Var (-x)" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "-" Operator, Tn "x" Variable]]) 
            == [UnaryIns UnaryOperator (Tn "a" Destination) (Tn "-" Operator) (Tn "x" Variable)]),

        check "Parse Unary: Negation Lit (-5)" 
            (getInstructions (parse [[Tn "b" Destination, Tn "=" Equals, Tn "-" Operator, Tn "5" Literal]]) 
            == [UnaryIns UnaryOperator (Tn "b" Destination) (Tn "-" Operator) (Tn "5" Literal)]),

        check "Parse Assignment: Variable to Destination" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "b" Variable]]) 
            == [AssignmentIns Assignment (Tn "a" Destination) (Tn "b" Variable)]),

        check "Parse Assignment: Literal to Destination" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "100" Literal]]) 
            == [AssignmentIns Assignment (Tn "a" Destination) (Tn "100" Literal)]),

        -- testing the live line extraction (lots of edge cases here)
        check "Parse Live Variables: Single" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "res" LiveSymbol]]) 
            == ["res"]),

        check "Parse Live Variables: Multiple (2)" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "a" LiveSymbol, Tn "b" LiveSymbol]]) 
            == ["a", "b"]),

        check "Parse Live Variables: Massive List (5)" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "a" LiveSymbol, Tn "b" LiveSymbol, Tn "c" LiveSymbol, Tn "d" LiveSymbol, Tn "e" LiveSymbol]]) 
            == ["a", "b", "c", "d", "e"]),

        check "Parse Live Variables: Missing Variables (Empty Live Line)" 
            (getLiveVariables (parse [[Tn "Live" Live]]) 
            == []),

        -- integration and breaking the parser
        check "Parse Empty Program (No tokens)" 
            (null (getInstructions (parse []))),

        check "Parse Multi-Line Integration (2 Instructions + Live)" 
            (let ast = parse [
                        [Tn "x" Destination, Tn "=" Equals, Tn "y" Variable, Tn "+" Operator, Tn "z" Variable],
                        [Tn "a" Destination, Tn "=" Equals, Tn "10" Literal],
                        [Tn "Live" Live, Tn "x" LiveSymbol, Tn "a" LiveSymbol]
                      ]
             in length (getInstructions ast) == 2 && getLiveVariables ast == ["x", "a"])
    ]