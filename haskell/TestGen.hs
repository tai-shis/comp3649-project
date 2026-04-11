import Control.Exception (SomeException, try)
import Gen (gen)

regCount :: Int
regCount = 8

testDir :: String
testDir = "test-input/"

runTest :: String -> IO ()
runTest inputFile = gen regCount (testDir ++ inputFile)

runTestExpectError :: String -> IO ()
runTestExpectError inputFile = do
  result <- try (runTest inputFile) :: IO (Either SomeException ())
  case result of
    Left ex -> putStrLn $ "Error successfully: " ++ show ex
    Right _  -> putStrLn $ "WARNING: Expected error but none was raised for " ++ inputFile

-- Tests expected to succeed and produce ASM output
testAssignments :: IO ()
testAssignments = runTest "assignments.txt"

testBinaryOpsWithLiterals :: IO ()
testBinaryOpsWithLiterals = runTest "binary_ops_with_literals.txt"

testBinaryOps :: IO ()
testBinaryOps = runTest "binary_ops.txt"

testChainedReuse :: IO ()
testChainedReuse = runTest "chained_reuse.txt"

testEmptyFile :: IO ()
testEmptyFile = runTest "empty_file.txt"

testMixedAllTypes :: IO ()
testMixedAllTypes = runTest "mixed_all_types.txt"

testMixedMany :: IO ()
testMixedMany = runTest "mixed_many.txt"

testMultipleLiveVars :: IO ()
testMultipleLiveVars = runTest "multiple_live_vars.txt"

testNoLiveDeclaration :: IO ()
testNoLiveDeclaration = runTest "no_live_declaration.txt"

testReferenceProgram :: IO ()
testReferenceProgram = runTest "reference_program.txt"

testSingleAssignment :: IO ()
testSingleAssignment = runTest "single_assignment.txt"

testSingleBinary :: IO ()
testSingleBinary = runTest "single_binary.txt"

testSingleUnary :: IO ()
testSingleUnary = runTest "single_unary.txt"

testUnaryOps :: IO ()
testUnaryOps = runTest "unary_ops.txt"

testUndefinedVariables :: IO ()
testUndefinedVariables = runTest "undefined_variables.txt"

-- Tests expected to raise errors
testInvalidOperators :: IO ()
testInvalidOperators = runTestExpectError "invalid_operators.txt"

testMalformedInMiddle :: IO ()
testMalformedInMiddle = runTestExpectError "malformed_in_middle.txt"

testMalformedSyntax :: IO ()
testMalformedSyntax = runTestExpectError "malformed_syntax.txt"

testMissingOperands :: IO ()
testMissingOperands = runTestExpectError "missing_operands.txt"

testValidThenInvalidOperator :: IO ()
testValidThenInvalidOperator = runTestExpectError "valid_then_invalid_operator.txt"

main :: IO ()
main = do
  putStrLn "=== Running TestGen ==="

  putStrLn "\n-- assignments (expect: ASM output) --"
  testAssignments

  putStrLn "\n-- binary_ops_with_literals (expect: ASM output) --"
  testBinaryOpsWithLiterals

  putStrLn "\n-- binary_ops (expect: ASM output) --"
  testBinaryOps

  putStrLn "\n-- chained_reuse (expect: ASM output) --"
  testChainedReuse

  putStrLn "\n-- empty_file (expect: empty .s file) --"
  testEmptyFile

  putStrLn "\n-- invalid_operators (expect: error) --"
  testInvalidOperators

  putStrLn "\n-- malformed_in_middle (expect: error) --"
  testMalformedInMiddle

  putStrLn "\n-- malformed_syntax (expect: error) --"
  testMalformedSyntax

  putStrLn "\n-- missing_operands (expect: error) --"
  testMissingOperands

  putStrLn "\n-- mixed_all_types (expect: ASM output) --"
  testMixedAllTypes

  putStrLn "\n-- mixed_many (expect: ASM output) --"
  testMixedMany

  putStrLn "\n-- multiple_live_vars (expect: ASM output) --"
  testMultipleLiveVars

  putStrLn "\n-- no_live_declaration (expect: ASM output, no MOV back to memory) --"
  testNoLiveDeclaration

  putStrLn "\n-- reference_program (expect: ASM output) --"
  testReferenceProgram

  putStrLn "\n-- single_assignment (expect: assignment then MOV to memory) --"
  testSingleAssignment

  putStrLn "\n-- single_binary (expect: MOV, ADD, MOV to memory) --"
  testSingleBinary

  putStrLn "\n-- single_unary (expect: MOV, MUL #-1, MOV) --"
  testSingleUnary

  putStrLn "\n-- unary_ops (expect: ASM output) --"
  testUnaryOps

  putStrLn "\n-- undefined_variables (expect: ASM output) --"
  testUndefinedVariables

  putStrLn "\n-- valid_then_invalid_operator (expect: error) --"
  testValidThenInvalidOperator

  putStrLn "\n=== TestGen complete ==="
