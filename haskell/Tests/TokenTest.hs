module Tests.TokenTest where
import Input.Token

-- simple wrapper
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name 

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results = 
    [
        -- making sure tokens build correctly
        check "build token and check value" (getValue (createToken "x" Destination) == "x"),
        check "build token and check type" (getType (createToken "x" Destination) == Destination),
        
        -- building every single type we have
        check "build variable token" (getType (createToken "a" Variable) == Variable),
        check "build literal token" (getType (createToken "42" Literal) == Literal),
        check "build operator token" (getType (createToken "+" Operator) == Operator),
        check "build equals token" (getType (createToken "=" Equals) == Equals),
        check "build live token" (getType (createToken "live:" Live) == Live),
        check "build livesymbol token" (getType (createToken "a," LiveSymbol) == LiveSymbol),
        check "build newline token" (getType (createToken "\n" Newline) == Newline),
        check "build eof token" (getType (createToken "" EOF) == EOF),
        
        -- grabbing values safely
        check "pull value from standard variable" (getValue (createToken "abc" Variable) == "abc"),
        check "pull value from eof is empty string" (getValue (createToken "" EOF) == ""),
        check "pull value from operator" (getValue (createToken "-" Operator) == "-"),
        
        -- grabbing types safely
        check "pull type destination" (getType (createToken "x" Destination) == Destination),
        check "pull type literal" (getType (createToken "99" Literal) == Literal),
        check "pull type eof" (getType (createToken "" EOF) == EOF),
        
        -- checking how token types print to strings
        check "print destination type" (show Destination == "Destination"),
        check "print variable type" (show Variable == "Variable"),
        check "print literal type" (show Literal == "Literal"),
        check "print operator type" (show Operator == "Operator"),
        check "print equals type" (show Equals == "Equals"),
        check "print live type" (show Live == "Live"),
        check "print livesymbol type" (show LiveSymbol == "LiveSymbol"),
        check "print newline type" (show Newline == "Newline"),
        check "print eof type" (show EOF == "EOF"),
        
        -- checking how full tokens print to strings
        check "print full variable token" (show (createToken "a" Variable) == "a : Variable"),
        check "print full literal token" (show (createToken "42" Literal) == "42 : Literal"),
        check "print full operator token" (show (createToken "+" Operator) == "+ : Operator"),
        check "print full eof token" (show (createToken "" EOF) == " : EOF"),
        
        -- equality logic
        check "identical tokens are equal" (createToken "x" Variable == createToken "x" Variable),
        check "different values aren't equal" (createToken "x" Variable /= createToken "y" Variable),
        check "different types aren't equal" (createToken "x" Destination /= createToken "x" Variable),
        check "completely different tokens aren't equal" (createToken "x" Destination /= createToken "10" Literal),
        
        check "identical types match" (Variable == Variable),
        check "different types mismatch" (Variable /= Destination)
    ]
