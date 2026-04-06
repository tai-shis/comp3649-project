module Tests.LivenessTest where

import Intermediate.Liveness hiding (Live)
import qualified Intermediate.Liveness as L
import Input.Instruction
import Input.Token
import Data.Set (Set, toList, empty, insert)

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- Sample tokens
destX :: Token
destX = createToken "x" Destination
 
destY :: Token
destY = createToken "y" Destination
 
varA :: Token
varA = createToken "a" Variable
 
varB :: Token
varB = createToken "b" Variable
 
litToken :: Token
litToken = createToken "42" Literal
 
addOp :: Token
addOp = createToken "+" Operator
 
-- Sample instructions
assignXA :: Instruction
assignXA = createInstruction (destX, varA)
 
assignXLit :: Instruction
assignXLit = createInstruction (destX, litToken)
 
assignYB :: Instruction
assignYB = createInstruction (destY, varB)
 
assignYX :: Instruction
assignYX = createInstruction (destY, createToken "x" Variable)
 
binaryXAB :: Instruction
binaryXAB = createInstruction (destX, varA, addOp, varB)

testLiveness :: IO ()
testLiveness = mapM_ putStrLn results

results :: [String]
results =
    [
        -- Show LivenessState
        check "Show Defined" (show (L.Defined "x") == "x: defined"),
        check "Show Live" (show (L.Live "x") == "x: live"),
        check "Show Unlive" (show (L.Unlive "x") == "x: unlive"),

        -- Eq LivenessState
        check "Eq - Defined == Defined, same name" (L.Defined "x" == L.Defined "x"),
        check "Eq - Live == Live, same name" (L.Live "x" == L.Live "x"),
        check "Eq - Unlive == Unlive, same name" (L.Unlive "x" == L.Unlive "x"),
        check "Eq - Defined == Live, same name" (L.Defined "x" == L.Live "x"),
        check "Eq - Live == Defined, same name" (L.Live "x" == L.Defined "x"),
        check "Eq - Defined == Unlive, same name" (L.Defined "x" == L.Unlive "x"),
        check "Eq - Live == Unlive, same name" (L.Live "x" == L.Unlive "x"),
        check "Eq - different names" (not (L.Defined "x" == L.Defined "y")),

        -- getLivenessName
        check "getLivenessName - Defined" (getLivenessName (L.Defined "x") == "x"),
        check "getLivenessName - Live" (getLivenessName (L.Live "x") == "x"),
        check "getLivenessName - Unlive" (getLivenessName (L.Unlive "x") == "x"),
        
        -- namesFromLiveness
        check "namesFromLiveness - empty list" (namesFromLiveness [] == []),
        check "namesFromLiveness - mixed states" (namesFromLiveness [L.Defined "x", L.Live "a", L.Unlive "b"] == ["x", "a", "b"]),
        
        -- isLive
        check "isLive - Live state" (isLive (L.Live "x") == True),
        check "isLive - Defined state" (isLive (L.Defined "x") == False),
        check "isLive - Unlive state" (isLive (L.Unlive "x") == False),
        
        -- isDefined
        check "isDefined - Defined state" (isDefined (L.Defined "x") == True),
        check "isDefined - Live state" (isDefined (L.Live "x") == False),
        check "isDefined - Unlive state" (isDefined (L.Unlive "x") == False),
        
        -- isUnlive
        check "isUnlive - Unlive state" (isUnlive (L.Unlive "x") == True),
        check "isUnlive - Live state" (isUnlive (L.Live "x") == False),
        check "isUnlive - Defined state" (isUnlive (L.Defined "x") == False),

        -- showLivenessStates
        check "showLivenessStates - empty list" (showLivenessStates [] == ""),
        check "showLivenessStates - single line" (showLivenessStates [[L.Defined "x", L.Live "a"]] == "x: defined, a: live\n"),
        check "showLivenessStates - multiple lines" (showLivenessStates [[L.Defined "x"], [L.Live "a"]] == "x: defined\na: live\n"),

        -- determineLiveness
        check "determineLiveness - empty instructions" (determineLiveness emptyInstructions == [[]]),
        check "determineLiveness - single assignment, operand live"
        -- x = a, live: a
        -- line 0: x defined, a live. line 1 (live section): a live
            (let liveness = determineLiveness (fromArraysInstructions [assignXA] ["a"])
                in isDefined (head (filter isDefined (liveness !! 0)))
                && isLive (head (filter isLive (liveness !! 0)))
                && getLivenessName (head (filter isDefined (liveness !! 0))) == "x"
                && getLivenessName (head (filter isLive (liveness !! 0))) == "a"),
        check "determineLiveness - single assignment, no live vars"
        -- x = a, no live vars. a should be unlive
            (let liveness = determineLiveness (fromArraysInstructions [assignXA] [])
            in any (\s -> isUnlive s && getLivenessName s == "a") (liveness !! 0)),
        check "determineLiveness - single binary instruction"
        -- x = a + b, live: a, b. x defined, a and b live
            (let liveness = determineLiveness (fromArraysInstructions [binaryXAB] ["a", "b"])
                 line0 = liveness !! 0
                in any (\s -> isDefined s && getLivenessName s == "x") line0
                    && any (\s -> isLive s && getLivenessName s == "a") line0
                    && any (\s -> isLive s && getLivenessName s == "b") line0),
        check "determineLiveness - variable defined then used"
            -- x = a, y = x, live: x. x defined on line 0, live on line 1
            (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYX] ["x"])
                in any (\s -> isDefined s && getLivenessName s == "x") (liveness !! 0)
                && any (\s -> isLive s && getLivenessName s == "x") (liveness !! 1)),
        check "determineLiveness - variable unlive after last use"
        -- x = a, y = b, live: b. a is unlive on line 0
        (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYB] ["b"])
            in any (\s -> isUnlive s && getLivenessName s == "a") (liveness !! 0)),
        check "determineLiveness - result length"
        -- 3 instructions + 1 live section = 4 entries
        (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYB, assignXLit] [])
         in length liveness == 4)
    ]
