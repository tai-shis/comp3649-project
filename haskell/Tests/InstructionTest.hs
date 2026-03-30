module InstructionTest where
import Token
import Instruction

testGetVariables :: IO ()
testGetVariables = do
    let inst1 = BinaryIns 
            BinaryOperator
            (Token "a" Destination)
            (Token "a" Variable)
            (Token "+" Operator)
            (Token "b" Variable)
    let inst1Vars = getVariables inst1
    print inst1Vars