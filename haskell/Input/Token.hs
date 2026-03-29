module Token (TokenType(..), Token(..)) where

data TokenType 
    = Destination
    | Variable
    | Literal
    | Operator
    | Equals
    | Live
    | LiveSymbol
    | Newline
    | EOF
    deriving (Show, Eq)

data Token = Token String TokenType
    deriving (Show, Eq)