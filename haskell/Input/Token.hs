module Token (
    TokenType(..), 
    Token(..), 
    getValue, 
    getType
) where

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
    deriving (Eq)

instance Show Token where
    show (Token value tokenType) = value ++ " : " ++ show tokenType

-- Public: Gets the value of a token
getValue :: Token -> String
getValue (Token value _) = value

-- Public: Gets the type of a token
getType :: Token -> TokenType
getType (Token _ tokenType) = tokenType
