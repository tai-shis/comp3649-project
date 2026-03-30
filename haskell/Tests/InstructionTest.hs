module InstructionTest where

import Input.Instruction
import Input.Token

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results = 
    []