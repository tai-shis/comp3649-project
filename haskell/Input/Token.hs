module Input.Token (
    TokenType(..), 
    Token, 
    getValue, 
    getType,
    createToken
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

data Token = Tn String TokenType
    deriving (Eq)

instance Show Token where
    show (Tn value tokenType) = value ++ " : " ++ show tokenType

-- Public: Creates a token given a value and type
createToken :: String -> TokenType -> Token
createToken value tokenType = Tn value tokenType

-- Public: Gets the value of a token
getValue :: Token -> String
getValue (Tn value _) = value

-- Public: Gets the type of a token
getType :: Token -> TokenType
getType (Tn _ tokenType) = tokenType