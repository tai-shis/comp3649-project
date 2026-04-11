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
        -- checking different math combinations
        check "add two variables" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "b" Variable, Tn "+" Operator, Tn "c" Variable]]) 
            == [BinaryIns BinaryOperator (Tn "a" Destination) (Tn "b" Variable) (Tn "+" Operator) (Tn "c" Variable)]),
            
        check "multiply variable by literal" 
            (getInstructions (parse [[Tn "t1" Destination, Tn "=" Equals, Tn "x" Variable, Tn "*" Operator, Tn "4" Literal]]) 
            == [BinaryIns BinaryOperator (Tn "t1" Destination) (Tn "x" Variable) (Tn "*" Operator) (Tn "4" Literal)]),

        check "divide literal by variable" 
            (getInstructions (parse [[Tn "t2" Destination, Tn "=" Equals, Tn "10" Literal, Tn "/" Operator, Tn "y" Variable]]) 
            == [BinaryIns BinaryOperator (Tn "t2" Destination) (Tn "10" Literal) (Tn "/" Operator) (Tn "y" Variable)]),

        check "subtract two literals" 
            (getInstructions (parse [[Tn "res" Destination, Tn "=" Equals, Tn "100" Literal, Tn "-" Operator, Tn "50" Literal]]) 
            == [BinaryIns BinaryOperator (Tn "res" Destination) (Tn "100" Literal) (Tn "-" Operator) (Tn "50" Literal)]),

        -- unary and basic assignments
        check "unary minus on a variable" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "-" Operator, Tn "x" Variable]]) 
            == [UnaryIns UnaryOperator (Tn "a" Destination) (Tn "-" Operator) (Tn "x" Variable)]),

        check "unary minus on a number" 
            (getInstructions (parse [[Tn "b" Destination, Tn "=" Equals, Tn "-" Operator, Tn "5" Literal]]) 
            == [UnaryIns UnaryOperator (Tn "b" Destination) (Tn "-" Operator) (Tn "5" Literal)]),

        check "assign var to dest" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "b" Variable]]) 
            == [AssignmentIns Assignment (Tn "a" Destination) (Tn "b" Variable)]),

        check "assign literal to dest" 
            (getInstructions (parse [[Tn "a" Destination, Tn "=" Equals, Tn "100" Literal]]) 
            == [AssignmentIns Assignment (Tn "a" Destination) (Tn "100" Literal)]),

        -- live variables (the tricky part)
        check "single live variable" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "res" LiveSymbol]]) 
            == ["res"]),

        check "two live variables" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "a" LiveSymbol, Tn "b" LiveSymbol]]) 
            == ["a", "b"]),

        check "lots of live variables at once" 
            (getLiveVariables (parse [[Tn "Live" Live, Tn "a" LiveSymbol, Tn "b" LiveSymbol, Tn "c" LiveSymbol, Tn "d" LiveSymbol, Tn "e" LiveSymbol]]) 
            == ["a", "b", "c", "d", "e"]),

        check "empty live line shouldn't break" 
            (getLiveVariables (parse [[Tn "Live" Live]]) 
            == []),

        -- integration and edge cases
        check "empty program shouldn't crash" 
            (null (getInstructions (parse []))),

        check "multi-line program with live vars" 
            (let ast = parse [
                        [Tn "x" Destination, Tn "=" Equals, Tn "y" Variable, Tn "+" Operator, Tn "z" Variable],
                        [Tn "a" Destination, Tn "=" Equals, Tn "10" Literal],
                        [Tn "Live" Live, Tn "x" LiveSymbol, Tn "a" LiveSymbol]
                      ]
             in length (getInstructions ast) == 2 && getLiveVariables ast == ["x", "a"])
    ]
