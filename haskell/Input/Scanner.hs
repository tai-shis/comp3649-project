module Input.Scanner(
    Scanner(..),
    ScanningState(..),
    scanNextLine
) where

import System.IO (Handle,
                  hIsEOF,
                  hGetLine,
                  hClose, 
                  openFile, 
                  IOMode(..))

import Input.Token hiding (TokenType(..))
import qualified Input.Token as T -- If needing to use TokenType for anything, prefix with T (i.e. "T.Live")

import Data.Char (isDigit)



data ScanningState = Instructions | Live | ScanEOF
    deriving (Show, Eq)

data Scanner = Scanner {
    fileHandle :: Handle,
    buffer :: [Token], -- Buffer of tokens for current line
    scanningState :: ScanningState
}

instance Eq Scanner where
    (Scanner _ _ state1) == (Scanner _ _ state2) = state1 == state2

-- List of possible operators
operators :: [Char]
operators = ['+', '-', '*', '/']

-- Invalid characters
invalidChars :: [Char]
invalidChars = ['$', '`', '"', '\'', '\\', '&', '^', '%', '#', '@', '!', '~', 
                '_', '[', ']', '{', '}', '|', ';', '<', '>', '?']

-- Delimiters that can be seen
delimiters :: [Char]
delimiters = ['\n', '=', ',', ' ', ':']

-- Public: creates a scanner object
createScanner :: FilePath -> IO Scanner
createScanner path = do
    handle <- openFile path ReadMode
    return Scanner { fileHandle = handle, buffer = [], scanningState = Instructions }

-- Public: Reads line from file and returns new instance of a Scanner.
scanNextLine :: Scanner -> IO Scanner
scanNextLine scanner = do
        eof <- hIsEOF (fileHandle scanner)
        if eof
            then return scanner { scanningState = ScanEOF } -- Return new scanner with EOF state
            else do
                line <- hGetLine (fileHandle scanner)
                let newScan = updateScanner scanner line
                return newScan

-- Private: gets the scanning state based on the token types given {Helper for updateScanner}
getState :: [Token] -> ScanningState
getState (token:_) =
    let tokenType = getType token
    in if tokenType /= T.Live && tokenType /= T.EOF
        then Instructions
        else Live

-- Private: Recursively scans characters and tokenizes them {Helper for tokenizeLine}
scanChars :: Scanner -> Bool -> [Char] -> [Token] -> String -> ([Token],[Char])
-- Base Case: No more characters in the line
scanChars scanner isDestination [] tokens symbol = 
    if null symbol
        then (tokens, []) -- Finished tokenizing, return final [Token]
        else (tokens ++ [tokenize scanner isDestination symbol], []) -- symbol had leftover contents, tokenize and return
-- Recursive Step: Processing next character
scanChars scanner isDestination (char:chars) tokens symbol
    | elem char invalidChars = error $ "Invalid character '" ++ [char] ++ "' found in input."
    | scanner == scanner { scanningState = Instructions } && char == ',' = error "Unexpected ',' found in input. Commans should only be found in live variable declarations."
    | elem char delimiters || elem char operators = 
        let
            -- Make sure symbol is present and tokenize it
            tokensWithSym = if not (null symbol) && symbol /= "live:" -- If symbol is not empty and not the live: token, tokenize it
                            then tokens ++ [tokenize scanner isDestination symbol]
                            else tokens
            
            -- Handle the current char if current char is an operator/singleton tokenizable, 
            finalTokens = if elem char ['+', '-', '*', '/', '=', '\n', ':', ','] -- If char is an operator or equals, tokenize it as well
                then 
                    if char == ':' then tokens ++ [tokenize scanner isDestination (symbol ++ [char])]
                    else tokensWithSym ++ [tokenize scanner isDestination [char]]
                else tokensWithSym -- If char is a delimiter, just tokenize the symbol and move on

            newIsDestination = if char == '=' then False else isDestination
        in scanChars scanner newIsDestination chars finalTokens "" -- Reset symbol so we can build the next one
    | otherwise = scanChars scanner isDestination chars tokens (symbol ++ [char]) -- Symbol has not been fully read; append char and keep going

-- Private: Tokenizes entire line {Helper for updateScanner}
tokenizeLine :: Scanner -> [Char] -> [Token]
tokenizeLine scanner line = 
    let tokens = fst (scanChars scanner True line [] "")
    in tokens 

-- Private: Updates the scanner state {called by scanNextLine}
updateScanner :: Scanner -> String -> Scanner
updateScanner scanner line =
    let tokens = tokenizeLine scanner line
    in let newState = getState tokens
    in scanner {buffer = tokens, scanningState = newState}

-- Private: Tokenizes a string into a token. If the string is not a valid token, throws an error.
tokenize :: Scanner -> Bool -> String -> Token
tokenize scanner isDestination str
    -- | scanner == scanner { scanningState = EOF } = T.Tn str T.EOF
    | str == "\n" = createToken str T.Newline
    | str == "=" = createToken str T.Equals
    | and (map isDigit str) = createToken str T.Literal
    | isOperator str = createToken str T.Operator
    | str == "live:" = createToken str T.Live
    -- if semicolon not part of "live:" keyword, we error
    | elem ':' str = error $ "Unexpected ':' found in token: '" ++ str ++ "'."
    -- now it has to be some sort of variable?
    | isValidVariable str = if scanner == scanner { scanningState = Live } 
                        then createToken str T.LiveSymbol
                        else if isDestination then createToken str T.Destination 
                        else createToken str T.Variable
    | otherwise = error $ "Invalid token: '" ++ str ++ "'."

-- Private: checks if a string is an operator (must be a single char and in the operators list)
isOperator :: String -> Bool
isOperator (c:[]) = elem c operators
isOperator _ = False

-- Private: Primitive check on a string after guards have been passed
isValidVariable :: String -> Bool
isValidVariable (c:cs) | isDigit c = False -- Variables cannot start with a digit
                       | otherwise = True
testScanner :: Scanner
testScanner = Scanner
    { fileHandle    = undefined  -- never touched by pure functions
    , buffer        = []
    , scanningState = Instructions
    }

-- Test tokenizeLine directly
main :: IO ()
main = do
    handle <- openFile "Tests/Test-Inputs/single-line.txt" ReadMode
    let scanner = Scanner { fileHandle = handle, buffer = [], scanningState = Instructions }
    scanAll scanner
    hClose handle

scanAll :: Scanner -> IO ()
scanAll scanner = do
    scanner' <- scanNextLine scanner
    if scanningState scanner' == ScanEOF
        then putStrLn "=== EOF ==="
        else do
            putStrLn $ "State:  " ++ show (scanningState scanner')
            putStrLn $ "Tokens: " ++ tokenListToString (buffer scanner')
            putStrLn ""
            scanAll scanner'