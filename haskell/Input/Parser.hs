module Input.Parser (
    parse
) where

import System.IO (
    Handle, 
    IOMode(ReadMode), 
    hClose, 
    openFile)

import Input.Scanner (
    Scanner(..), 
    scanNextLine, 
    createScanner, 
    isEOF)

import Input.Token (
    Token(Tn), 
    TokenType(..), 
    tokenListToString, 
    isLiveSymbol)

import Input.Instruction (
    Instruction, 
    Instructions, 
    createInstruction,
    fromArraysInstructions)

-- Private: Parse through tokens and validate them.
parseTokens :: [[Token]] -> Bool -> ([Instruction], [String])
parseTokens [] _ = ([], [])
parseTokens _ True = error "Error: Unexpected tokens found after live line."

-- Binary instruction: dest = op1 operator op2
parseTokens ((dest@(Tn _ Destination) : (Tn _ Equals) : op1 : operator@(Tn _ Operator) : op2 : []) : rest) False
    | (Tn _ Variable) <- op1, (Tn _ Variable) <- op2 = binary op1 op2
    | (Tn _ Variable) <- op1, (Tn _ Literal)  <- op2 = binary op1 op2
    | (Tn _ Literal)  <- op1, (Tn _ Variable) <- op2 = binary op1 op2
    | (Tn _ Literal)  <- op1, (Tn _ Literal)  <- op2 = binary op1 op2
    where binary a b =
            let (restInstructions, restTokens) = parseTokens rest False
            in (createInstruction (dest, a, operator, b) : restInstructions, restTokens)

-- Unary instruction: dest = operator op
parseTokens ((dest@(Tn _ Destination) : (Tn _ Equals) : operator@(Tn _ Operator) : op : []) : rest) False
    | (Tn _ Variable) <- op = unary op
    | (Tn _ Literal)  <- op = unary op
    where unary a =
            let (restInstructions, restTokens) = parseTokens rest False
            in (createInstruction (dest, operator, a) : restInstructions, restTokens)

-- Assignment instruction: dest = op
parseTokens ((dest@(Tn _ Destination) : (Tn _ Equals) : op : []) : rest) False
    | (Tn _ Variable) <- op = assign op
    | (Tn _ Literal)  <- op = assign op
    where assign a =
            let (restInstructions, restTokens) = parseTokens rest False
            in (createInstruction (dest, a) : restInstructions, restTokens)

-- Live line
parseTokens (((Tn _ Live) : tokens) : rest) False =
    if checkLiveTokens tokens
        then (restInstructions, map (\(Tn name _) -> name) tokens)
        else error "Error: Invalid tokens in live line encountered."
    where (restInstructions, _) = parseTokens rest True

parseTokens _ _ = error "Error: Invalid instruction format encountered."

-- Public: Parse tokens into Instructions
parse :: [[Token]] -> Instructions
parse tokenLines = fromArraysInstructions instructions liveTokens
    where (instructions, liveTokens) = parseTokens tokenLines False

checkLiveTokens :: [Token] -> Bool
checkLiveTokens [] = True
checkLiveTokens (t:ts) | isLiveSymbol t = True && checkLiveTokens ts
                       | otherwise = False
