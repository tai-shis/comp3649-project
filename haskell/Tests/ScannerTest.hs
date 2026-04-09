-- ScannerTest.hs
-- Test suite for Input.Scanner (updated Scanner.hs)
--
-- Assumptions about Input.Token (Token.hs was not available at time of writing):
--   - `createToken :: String -> T.TokenType -> Token`   constructs a Token
--   - `getType     :: Token  -> T.TokenType`            returns the token's type tag
--   - `getValue    :: Token  -> String`                 returns the token's raw string value
--   - `tokenListToString :: [Token] -> String`          used in Scanner's own main
--   - TokenType constructors used: T.Live, T.EOF, T.Equals, T.Literal, T.Operator,
--                                  T.Destination, T.Variable, T.LiveSymbol, T.Newline
--   - Token derives (Show, Eq)
--
-- How to build & run (from project root):
--   ghc --make -isrc tests/ScannerTest.hs -o tests/ScannerTest && ./tests/ScannerTest
--
-- Input files are expected at:  tests/inputs/<name>.txt
--
-- Each test prints [PASS] or [FAIL]. Exit code 1 if any test fails.

module Tests.ScannerTest where

import System.IO        (openFile, hClose, IOMode(ReadMode))
import System.Exit      (exitFailure, exitSuccess)
import Control.Exception (evaluate, try, SomeException)

import Input.Scanner
import Input.Token      hiding (TokenType(..))
import qualified Input.Token as T

-- ---------------------------------------------------------------------------
-- Minimal test harness
-- ---------------------------------------------------------------------------

type TestResult = (String, Bool)

runTest :: String -> Bool -> IO TestResult
runTest desc result = do
    let tag = if result then "PASS" else "FAIL"
    putStrLn $ "[" ++ tag ++ "] " ++ desc
    return (desc, result)

-- Run a test that is expected to throw an error. Passes if evaluation throws.
runErrorTest :: String -> IO a -> IO TestResult
runErrorTest desc action = do
    result <- try (action >> return ()) :: IO (Either SomeException ())
    case result of
        Left  _ -> runTest desc True
        Right _ -> runTest desc False

summarise :: [TestResult] -> IO ()
summarise results = do
    let failures = filter (not . snd) results
    putStrLn $ replicate 60 '-'
    putStrLn $ "Results: " ++ show (length results) ++ " tests, "
                            ++ show (length failures) ++ " failure(s)."
    if null failures
        then putStrLn "All tests passed." >> exitSuccess
        else do
            putStrLn "Failed tests:"
            mapM_ (\(d, _) -> putStrLn $ "  * " ++ d) failures
            exitFailure

-- ---------------------------------------------------------------------------
-- Helpers
-- ---------------------------------------------------------------------------

inputsDir :: FilePath
inputsDir = "Tests/"

isState :: String -> Scanner -> Bool
isState expected sc = show (scanningState sc) == expected

-- Open a file and wrap it in a fresh Scanner in Instructions state.
makeScanner :: FilePath -> IO Scanner
makeScanner path = do
    h <- openFile (inputsDir ++ path) ReadMode
    return Scanner { fileHandle = h, buffer = [], scanningState = Instructions }

-- Convenience: extract raw string values from a buffer.
tokenValues :: [Token] -> [String]
tokenValues = map getValue

-- Convenience: extract token types from a buffer.
tokenTypes :: [Token] -> [T.TokenType]
tokenTypes = map getType

-- ---------------------------------------------------------------------------
-- Tests
-- ---------------------------------------------------------------------------

-- T01: Empty file → ScanEOF immediately
testEmptyFileEOF :: IO TestResult
testEmptyFileEOF = do
    sc  <- makeScanner "Test-Inputs/empty.txt"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T01 – Empty file: scanningState = ScanEOF"
        (isState "ScanEOF" sc')

-- T02: Single-line file → first call tokenizes, second call gives ScanEOF
testSingleLineSecondCallEOF :: IO TestResult
testSingleLineSecondCallEOF = do
    sc  <- makeScanner "Test-Inputs/single-line.txt"   -- "live: x = 1"
    sc1 <- scanNextLine sc
    sc2 <- scanNextLine sc1
    hClose (fileHandle sc2)
    runTest "T02 – Single-line file: second scanNextLine = ScanEOF"
        (not (isState "ScanEOF" sc1) && isState "ScanEOF" sc2)

-- T03: Line beginning with live: → Live state
testStateLive :: IO TestResult
testStateLive = do
    sc  <- makeScanner "Test-Inputs/single-line.txt"   -- "live: x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T03 – 'live: x = 1': scanningState = Live"
        (isState "Live" sc')

-- T04: Line beginning with non-live token → Instructions state
testStateInstructions :: IO TestResult
testStateInstructions = do
    sc  <- makeScanner "Test-Inputs/instructions-line.txt"   -- "add x, y"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T04 – 'add x, y': scanningState = Instructions"
        (isState "Instructions" sc')

-- T05: Space is a delimiter but produces no token
testSpaceNoToken :: IO TestResult
testSpaceNoToken = do
    sc  <- makeScanner "Test-Inputs/space-delim.txt"   -- "x y"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T05 – 'x y': tokens are [x, y], no space token"
        (tokenValues (buffer sc') == ["x", "y"])

-- T06: Comma is a delimiter but produces no token
testCommaNoToken :: IO TestResult
testCommaNoToken = do
    sc  <- makeScanner "Test-Inputs/comma-delim.txt"   -- "x,y"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T06 – 'x,y': tokens are [x, y], no comma token"
        (tokenValues (buffer sc') == ["x", "y"])

-- T07: '=' produces an Equals token and splits surrounding symbols
testEqualsTokenized :: IO TestResult
testEqualsTokenized = do
    sc  <- makeScanner "Test-Inputs/test-equals.txt"   -- "x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    let vals  = tokenValues (buffer sc')
        types = tokenTypes  (buffer sc')
    runTest "T07 – 'x = 1': tokens [x(Destination), =(Equals), 1(Literal)]"
        (vals  == ["x", "=", "1"] &&
         types == [T.Destination, T.Equals, T.Literal])

-- T08: 'live:' colon is consumed as part of the Live token, not standalone
testColonInLiveToken :: IO TestResult
testColonInLiveToken = do
    sc  <- makeScanner "Test-Inputs/single-line.txt"   -- "live: x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    let vals = tokenValues (buffer sc')
    runTest "T08 – 'live: x = 1': first token is 'live:', no standalone ':'"
        (case vals of
            (v:_) -> v == "live:" && ":" `notElem` vals
            []    -> False)

-- T09: Bare ':' not part of 'live:' throws an error
testBareColonError :: IO TestResult
testBareColonError =
    runErrorTest "T09 – 'x: y': bare ':' throws an error" $ do
        sc  <- makeScanner "test_bare_colon.txt"   -- "x: y"
        sc' <- scanNextLine sc
        hClose (fileHandle sc')
        -- force evaluation of the buffer to trigger the error
        return $! length (buffer sc')

-- T10: Single operator between symbols
testSimpleOperator :: IO TestResult
testSimpleOperator = do
    sc  <- makeScanner "Test-Inputs/simple-op.txt"   -- "a+b"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T10 – 'a+b': tokens are [a, +, b]"
        (tokenValues (buffer sc') == ["a", "+", "b"])

-- T11: All four operators in one expression
testAllOperators :: IO TestResult
testAllOperators = do
    sc  <- makeScanner "Test-Inputs/all-ops.txt"   -- "a+b-c*d/e"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T11 – 'a+b-c*d/e': nine tokens in order"
        (tokenValues (buffer sc') == ["a","+","b","-","c","*","d","/","e"])

-- T12: Operator at the start — no empty token before it
testOperatorAtStart :: IO TestResult
testOperatorAtStart = do
    sc  <- makeScanner "Test-Inputs/op-start.txt"   -- "+x"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T12 – '+x': tokens are [+, x], no empty token before +"
        (tokenValues (buffer sc') == ["+", "x"])

-- T13: Operator at the end — no empty token after it
testOperatorAtEnd :: IO TestResult
testOperatorAtEnd = do
    sc  <- makeScanner "Test-Inputs/op-end.txt"   -- "x+"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T13 – 'x+': tokens are [x, +], no empty token after +"
        (tokenValues (buffer sc') == ["x", "+"])

-- T14: Invalid character in input throws an error
testInvalidCharError :: IO TestResult
testInvalidCharError =
    runErrorTest "T14 – 'x$y': invalid char '$' throws an error" $ do
        sc  <- makeScanner "Test-Inputs/invalid-embedded.txt"   -- "x$y"
        sc' <- scanNextLine sc
        hClose (fileHandle sc')
        return $! length (buffer sc')

-- T15: Line of entirely invalid chars throws an error
testAllInvalidCharsError :: IO TestResult
testAllInvalidCharsError =
    runErrorTest "T15 – '$!@#': all-invalid line throws an error" $ do
        sc  <- makeScanner "Test-Inputs/invalid-chars.txt"   -- "$!@#"
        sc' <- scanNextLine sc
        hClose (fileHandle sc')
        return $! length (buffer sc')

-- T16: All-digit string → Literal token
testLiteralToken :: IO TestResult
testLiteralToken = do
    sc  <- makeScanner "Test-Inputs/test-number.txt"   -- "123"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    let toks = buffer sc'
    runTest "T16 – '123': single Literal token"
        (tokenValues toks == ["123"] && tokenTypes toks == [T.Literal])

-- T17: First variable before '=' in Instructions state → Destination
testDestinationToken :: IO TestResult
testDestinationToken = do
    sc  <- makeScanner "Test-Inputs/test-equals.txt"   -- "x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T17 – 'x = 1': 'x' typed as Destination"
        (case buffer sc' of
            (t:_) -> getType t == T.Destination
            []    -> False)

-- T18: Variable after '=' in Instructions state → Variable
testVariableToken :: IO TestResult
testVariableToken = do
    sc  <- makeScanner "Test-Inputs/var-after-equals.txt"   -- "result = x"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    let types = tokenTypes (buffer sc')
    runTest "T18 – 'result = x': 'x' after '=' typed as Variable"
        (last types == T.Variable)

-- T19: Variable in Live-state scanner → LiveSymbol
testLiveSymbolToken :: IO TestResult
testLiveSymbolToken = do
    sc  <- makeScanner "Test-Inputs/single-line.txt"   -- "live: x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    -- buffer: [live:(Live), x(LiveSymbol), =(Equals), 1(Literal)]
    let types = tokenTypes (buffer sc')
    runTest "T19 – 'live: x = 1': 'x' typed as LiveSymbol"
        (types !! 1 == T.LiveSymbol)

-- T20: Operator char produces Operator token type
testOperatorTokenType :: IO TestResult
testOperatorTokenType = do
    sc  <- makeScanner "Test-Inputs/simple-op.txt"   -- "a+b"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T20 – 'a+b': '+' has type Operator"
        (tokenTypes (buffer sc') !! 1 == T.Operator)

-- T21: '=' produces Equals token type
testEqualsTokenType :: IO TestResult
testEqualsTokenType = do
    sc  <- makeScanner "Test-Inputs/test-equals.txt"   -- "x = 1"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T21 – 'x = 1': '=' has type Equals"
        (tokenTypes (buffer sc') !! 1 == T.Equals)

-- T22: Symbol with no trailing delimiter is flushed at end of line
testLeftoverSymbolFlushed :: IO TestResult
testLeftoverSymbolFlushed = do
    sc  <- makeScanner "Test-Inputs/test-leftover.txt"   -- "abc"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T22 – 'abc': leftover symbol flushed as single token"
        (tokenValues (buffer sc') == ["abc"])

-- T23: Digit-leading variable name throws an error
testDigitLeadingVarError :: IO TestResult
testDigitLeadingVarError =
    runErrorTest "T23 – '1x = 2': digit-leading variable throws an error" $ do
        sc  <- makeScanner "Test-Inputs/digit-leading.txt"   -- "1x = 2"
        sc' <- scanNextLine sc
        hClose (fileHandle sc')
        return $! length (buffer sc')

-- T24: Blank line → empty buffer
testEmptyLine :: IO TestResult
testEmptyLine = do
    sc  <- makeScanner "Test-Inputs/blank-line.txt"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T24 – blank line: buffer = []"
        (null (buffer sc'))

-- T25: Whitespace-only line → empty buffer
testWhitespaceOnlyLine :: IO TestResult
testWhitespaceOnlyLine = do
    sc  <- makeScanner "Test-Inputs/whitespace-line.txt"   -- "   "
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    runTest "T25 – '   ': buffer = []"
        (null (buffer sc'))

-- T26: Full live: instruction with operators — values and types
testLiveInstructionLine :: IO TestResult
testLiveInstructionLine = do
    sc  <- makeScanner "Test-Inputs/live-instruction.txt"   -- "live: result = a+b"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    let vals  = tokenValues (buffer sc')
        types = tokenTypes  (buffer sc')
    runTest "T26 – 'live: result = a+b': correct tokens, types, and Live state"
        (vals  == ["live:", "result", "=", "a", "+", "b"] &&
         types == [T.Live, T.LiveSymbol, T.Equals, T.LiveSymbol, T.Operator, T.LiveSymbol] &&
         isState "Live" sc')

-- T27: Multi-line file — each scanNextLine produces the correct buffer
testMultipleLines :: IO TestResult
testMultipleLines = do
    sc  <- makeScanner "Test-Inputs/multi-line.txt"
    -- Line 1: "add x, y"
    sc1 <- scanNextLine sc
    -- Line 2: "live: result = a+b-c*d/e"
    sc2 <- scanNextLine sc1
    -- Line 3: "x1 = 123"  — NOTE: '1' suffix is fine as long as symbol starts with letter
    sc3 <- scanNextLine sc2
    hClose (fileHandle sc3)
    let v1 = tokenValues (buffer sc1)
        v2 = tokenValues (buffer sc2)
        v3 = tokenValues (buffer sc3)
    runTest "T27 – multiline: each scanNextLine produces the correct buffer"
        (v1 == ["add", "x", "y"] &&
         v2 == ["live:", "result", "=", "a", "+", "b", "-", "c", "*", "d", "/", "e"] &&
         v3 == ["x1", "=", "123"])

-- ---------------------------------------------------------------------------
-- Main
-- ---------------------------------------------------------------------------

main :: IO ()
main = do
    putStrLn $ replicate 60 '='
    putStrLn "Scanner Test Suite"
    putStrLn $ replicate 60 '='
    results <- sequence
        [ testEmptyFileEOF,
          testSingleLineSecondCallEOF,
          testStateLive,
          testStateInstructions,
          testSpaceNoToken,
          testCommaNoToken,
          testEqualsTokenized,
          testColonInLiveToken,
          testBareColonError,
          testSimpleOperator,
          testAllOperators,
          testOperatorAtStart,
          testOperatorAtEnd,
          testInvalidCharError,
          testAllInvalidCharsError,
          testLiteralToken,
          testDestinationToken,
          testVariableToken,
          testLiveSymbolToken,
          testOperatorTokenType,
          testEqualsTokenType,
          testLeftoverSymbolFlushed,
          testDigitLeadingVarError,
          testEmptyLine,
          testWhitespaceOnlyLine,
          testLiveInstructionLine,
          testMultipleLines
        ]
    summarise results