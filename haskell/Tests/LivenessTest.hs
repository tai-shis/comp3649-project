module Tests.LivenessTest where

import Intermediate.Liveness hiding (Live)
import qualified Intermediate.Liveness as L
import Input.Instruction
import Input.Token
import Data.Set (Set, toList, empty, insert)

-- simple wrapper to keep outputs consistent
check :: String -> Bool -> String
check name True = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- setting up some dummy tokens so we don't have to parse strings
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
 
-- dummy instructions
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

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results =
    [
        -- printing liveness states
        check "print defined state" (show (L.Defined "x") == "x: defined"),
        check "print live state" (show (L.Live "x") == "x: live"),
        check "print unlive state" (show (L.Unlive "x") == "x: unlive"),

        -- checking equality logic
        check "same defined states are equal" (L.Defined "x" == L.Defined "x"),
        check "same live states are equal" (L.Live "x" == L.Live "x"),
        check "same unlive states are equal" (L.Unlive "x" == L.Unlive "x"),
        check "defined and live aren't equal" (L.Defined "x" == L.Live "x"),
        check "live and defined aren't equal" (L.Live "x" == L.Defined "x"),
        check "defined and unlive aren't equal" (L.Defined "x" == L.Unlive "x"),
        check "live and unlive aren't equal" (L.Live "x" == L.Unlive "x"),
        check "different variables aren't equal" (not (L.Defined "x" == L.Defined "y")),

        -- pulling names out of the state wrappers
        check "extract name from defined" (getLivenessName (L.Defined "x") == "x"),
        check "extract name from live" (getLivenessName (L.Live "x") == "x"),
        check "extract name from unlive" (getLivenessName (L.Unlive "x") == "x"),
        
        check "extract names from empty list" (namesFromLiveness [] == []),
        check "extract names from mixed list" (namesFromLiveness [L.Defined "x", L.Live "a", L.Unlive "b"] == ["x", "a", "b"]),
        
        -- boolean checks for specific states
        check "isLive catches live state" (isLive (L.Live "x") == True),
        check "isLive rejects defined" (isLive (L.Defined "x") == False),
        check "isLive rejects unlive" (isLive (L.Unlive "x") == False),
        
        check "isDefined catches defined state" (isDefined (L.Defined "x") == True),
        check "isDefined rejects live" (isDefined (L.Live "x") == False),
        check "isDefined rejects unlive" (isDefined (L.Unlive "x") == False),
        
        check "isUnlive catches unlive state" (isUnlive (L.Unlive "x") == True),
        check "isUnlive rejects live" (isUnlive (L.Live "x") == False),
        check "isUnlive rejects defined" (isUnlive (L.Defined "x") == False),

        -- printing full lists of states
        check "print empty state list" (showLivenessStates [] == ""),
        check "print single line of states" (showLivenessStates [[L.Defined "x", L.Live "a"]] == "x: defined, a: live\n"),
        check "print multiple lines of states" (showLivenessStates [[L.Defined "x"], [L.Live "a"]] == "x: defined\na: live\n"),

        -- the massive determineLiveness function (core logic)
        check "liveness builder on empty program" (determineLiveness emptyInstructions == [[]]),
        
        check "single assignment keeps operand live"
        -- program: x = a, live: a
        -- so on line 0: x is defined, a is live. 
            (let liveness = determineLiveness (fromArraysInstructions [assignXA] ["a"])
                in isDefined (head (filter isDefined (liveness !! 0)))
                && isLive (head (filter isLive (liveness !! 0)))
                && getLivenessName (head (filter isDefined (liveness !! 0))) == "x"
                && getLivenessName (head (filter isLive (liveness !! 0))) == "a"),
                
        check "operand dies if not in live section"
        -- program: x = a, live: (empty)
        -- a should be marked as unlive immediately
            (let liveness = determineLiveness (fromArraysInstructions [assignXA] [])
            in any (\s -> isUnlive s && getLivenessName s == "a") (liveness !! 0)),
            
        check "binary instruction keeps both operands live"
        -- program: x = a + b, live: a, b
            (let liveness = determineLiveness (fromArraysInstructions [binaryXAB] ["a", "b"])
                 line0 = liveness !! 0
                in any (\s -> isDefined s && getLivenessName s == "x") line0
                    && any (\s -> isLive s && getLivenessName s == "a") line0
                    && any (\s -> isLive s && getLivenessName s == "b") line0),
                    
        check "variable is defined then used later"
            -- program: x = a, y = x, live: x. 
            -- x is defined line 0, but live on line 1
            (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYX] ["x"])
                in any (\s -> isDefined s && getLivenessName s == "x") (liveness !! 0)
                && any (\s -> isLive s && getLivenessName s == "x") (liveness !! 1)),
                
        check "variable drops to unlive after its final use"
        -- program: x = a, y = b, live: b
        -- a is never used again, should die on line 0
        (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYB] ["b"])
            in any (\s -> isUnlive s && getLivenessName s == "a") (liveness !! 0)),
            
        check "liveness array matches instruction count plus live line"
        -- 3 instructions + 1 live section at the bottom = 4 lines total
        (let liveness = determineLiveness (fromArraysInstructions [assignXA, assignYB, assignXLit] [])
         in length liveness == 4)
    ]