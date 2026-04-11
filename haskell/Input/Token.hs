module Input.Token (
    TokenType(..), 
    Token(..), 
    getValue, 
    getType,
    createToken,
    tokenListToString,
    isLiveSymbol
) where

import Lib.Helper (commaSeparatedList)

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

data Token = Tn String TokenType
    deriving (Eq)

instance Show Token where
    show (Tn value tokenType) = value ++ " : " ++ show tokenType

-- Public: Shows a list of tokens as a comma-separated string
tokenListToString :: [Token] -> String
tokenListToString tokens = commaSeparatedList tokens

-- Public: Creates a token given a value and type
createToken :: String -> TokenType -> Token
createToken value tokenType = Tn value tokenType

-- Public: Gets the value of a token
getValue :: Token -> String
getValue (Tn value _) = value

-- Public: Gets the type of a token
getType :: Token -> TokenType
getType (Tn _ tokenType) = tokenType

-- Public: checks if a token is a live symbol
isLiveSymbol :: Token -> Bool
isLiveSymbol token = getType token == LiveSymbol