module TokenTest where
import Input.Token

check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name 

testToken :: IO ()
testToken = mapM_ putStrLn results

results :: [String]
results = 
    [
        -- createToken
        check "createToken - getValue returns correct value" (getValue (createToken "x" Destination) == "x"),
        check "createToken - getType returns correct type" (getType (createToken "x" Destination) == Destination),
        check "createToken - Variable token" (getType (createToken "a" Variable) == Variable),
        check "createToken - Literal token" (getType (createToken "42" Literal) == Literal),
        check "createToken - Operator token" (getType (createToken "+" Operator) == Operator),
        check "createToken - Equals token" (getType (createToken "=" Equals) == Equals),
        check "createToken - Live token" (getType (createToken "live:" Live) == Live),
        check "createToken - LiveSymbol token" (getType (createToken "a," LiveSymbol) == LiveSymbol),
        check "createToken - Newline token" (getType (createToken "\n" Newline) == Newline),
        check "createToken - EOF token" (getType (createToken "" EOF) == EOF),
        -- getValue
        check "getValue - variable name" (getValue (createToken "abc" Variable) == "abc"),
        check "getValue - empty string" (getValue (createToken "" EOF) == ""),
        check "getValue - operator symbol" (getValue (createToken "-" Operator) == "-"),
        -- getType
        check "getType - Destination" (getType (createToken "x" Destination) == Destination),
        check "getType - Literal" (getType (createToken "99" Literal) == Literal),
        check "getType - EOF" (getType (createToken "" EOF) == EOF),
        -- Show TokenType
        check "Show TokenType - Destination" (show Destination == "Destination"),
        check "Show TokenType - Variable" (show Variable == "Variable"),
        check "Show TokenType - Literal" (show Literal == "Literal"),
        check "Show TokenType - Operator" (show Operator == "Operator"),
        check "Show TokenType - Equals" (show Equals == "Equals"),
        check "Show TokenType - Live" (show Live == "Live"),
        check "Show TokenType - LiveSymbol" (show LiveSymbol == "LiveSymbol"),
        check "Show TokenType - Newline" (show Newline == "Newline"),
        check "Show TokenType - EOF" (show EOF == "EOF"),
        -- Show Token
        check "Show Token - Variable" (show (createToken "a" Variable) == "a : Variable"),
        check "Show Token - Literal" (show (createToken "42" Literal) == "42 : Literal"),
        check "Show Literal - Operator" (show (createToken "+" Operator) == "+ : Operator"),
        check "Show EOF - Operator" (show (createToken "" EOF) == " : EOF"),
        -- Eq Token
        check "Eq Token - equal tokens" (createToken "x" Variable == createToken "x" Variable),
        check "Eq Token - different values" (createToken "x" Variable /= createToken "y" Variable),
        check "Eq Token - different types" (createToken "x" Destination /= createToken "x" Variable),
        check "Eq Token - value & type unequal" (createToken "x" Destination /= createToken "10" Literal),
        -- Eq TokenType
        check "Eq TokenType - equal types" (Variable == Variable),
        check "Eq TokenType - unequal types" (Variable /= Destination)
    ]
