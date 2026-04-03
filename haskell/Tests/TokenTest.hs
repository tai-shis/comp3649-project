module TokenTest where

import Input.Token

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results =
    -- Construction tests (verify Eq holds against expected value)
    [ check "Token construction - variable"    (Token "x" Variable    == Token "x" Variable)
    , check "Token construction - literal"     (Token "42" Literal    == Token "42" Literal)
    , check "Token construction - operator"    (Token "+" Operator    == Token "+" Operator)
    , check "Token construction - destination" (Token "dest" Destination == Token "dest" Destination)
    , check "Token construction - EOF"         (Token "" EOF          == Token "" EOF)

    -- Show TokenType
    , check "Show TokenType - Variable"  (show Variable  == "Variable")
    , check "Show TokenType - Operator"  (show Operator  == "Operator")
    , check "Show TokenType - Newline"   (show Newline   == "Newline")
    , check "Show TokenType - Live" (show Live == "Live")
    , check "Show TokenType - EOF"       (show EOF       == "EOF")

    -- Show Token
    , check "Show Token" (show (Token "x" Variable) == "Token \"x\" Variable")

    -- Eq TokenType
    , check "Eq TokenType - equal types"   (Variable == Variable)
    , check "Eq TokenType - unequal types" (Variable /= Literal)

    -- Eq Token
    , check "Eq Token - equal tokens"      (Token "x" Variable == Token "x" Variable)
    , check "Eq Token - different string"  (Token "x" Variable /= Token "y" Variable)
    , check "Eq Token - different type"    (Token "x" Variable /= Token "x" Literal)
    , check "Eq Token - both fields differ" (Token "x" Variable /= Token "42" Literal)
    ]