module Input.Scanner(
    scanNextLine
) where

import System.IO (Handle,
                  hIsEOF,
                  hGetLine)
import Input.Token hiding (TokenType(..))
import qualified Input.Token as T -- If needing to use TokenType for anything, prefix with T (i.e. "T.Live")

data ScanningState = Instructions | Live | EOF
    deriving (Show, Eq)

data Scanner = Scanner {
    fileHandle :: Handle,
    buffer :: [Token], -- Buffer of tokens for current line
    scanningState :: ScanningState
}

-- List of possible operators
operators :: [Char]
operators = ['+', '-', '*', '/']

-- Invalid characters
invalidChars :: [Char]
invalidChars = ['$', '`', '"', '\'', '\\', '&', '^', '%', '#', '@', '!', '~', 
                '_', '[', ']', '{', '}', '|', ';', '<', '>', '?']

-- Delimiters that can be seen
delimiters :: [Char]
delimiters = ['\n', '=', ',', ' ']

-- Public: Reads line from file and returns new instance of a Scanner.
scanNextLine :: Scanner -> IO Scanner
scanNextLine scanner = do
        eof <- hIsEOF (fileHandle scanner)
        if eof
            then return scanner { scanningState = EOF } -- Return new scanner with EOF state
            else do
                line <- hGetLine (fileHandle scanner)
                scanner <- updateScanner scanner line
                return scanner

-- Private: gets the scanning state based on the token types given {Helper for updateScanner}
getState :: [Token] -> ScanningState
getState (token:_) =
    let tokenType = getType token
    in if tokenType /= T.Live && tokenType /= T.EOF
        then Instructions
        else Live

-- Private: Recursively scans characters and tokenizes them {Helper for tokenizeLine}
-- TODO: Not finished, not sure if any of the code in here is going to work so do not trust it!
scanChars :: [Char] -> [Token] -> String -> ([Token],[Char])
-- Base Case: No more characters in the line
scanChars [] tokens symbol = 
    if null symbol
        then (tokens, []) -- Finished tokenizing, return final [Token]
        else (tokens ++ [tokenize symbol], []) -- symbol had leftover contents, tokenize and return
-- Recursive Step: Processing next character
scanChars (char:chars) tokens symbol
    | char `elem` delimiters || char `elem` operators = 
        let
            -- Make sure symbol is present and tokenize it
            tokensWithSym = if not (null symbol)
                            then tokens ++ [tokenize symbol]
                            else tokens
            
            -- Handle the current char
            finalTokens = if char `notElem` invalidChars && char `notElem` [' ', ',']
                          then tokensWithSym ++ [tokenize [char]]
                          else tokensWithSym
        in scanChars chars finalTokens "" -- Reset symbol so we can build the next one
    | otherwise = scanChars chars tokens (symbol ++ [char]) -- Symbol has not been fully read; append char and keep going


-- Private: Tokenizes entire line {Helper for updateScanner}
tokenizeLine :: [Char] -> [Token]
tokenizeLine line = 
    let tokens = fst (scanChars line [] "")
    in tokens 

-- Private: Updates the scanner state {called by scanNextLine}
updateScanner:: Scanner -> String -> Scanner
updateScanner scanner line =
    let tokens = tokenizeLine line
    in let newState = getState tokens
    in scanner {buffer = tokens, scanningState = newState}
