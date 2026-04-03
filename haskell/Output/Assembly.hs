module Output.Assembly (OpCode, AssemblyInstruction, Assembly) where

data OpCode 
    = ADD
    | SUB 
    | MUL 
    | DIV
    | MOV
    deriving (Eq)

instance Show OpCode where
    show ADD = "ADD"
    show SUB = "SUB"
    show MUL = "MUL"
    show DIV = "DIV"
    show MOV = "MOV"

type Dest = String
type Src = String

data AssemblyInstruction = AssemblyInstruction OpCode Dest Src
    deriving (Eq)

instance Show AssemblyInstruction where
    show (AssemblyInstruction op dest src) = show op ++ " " ++ dest ++ "," ++ src


data Assembly = Assembly [AssemblyInstruction]

instance Show Assembly where
    show (Assembly instructions) = "Assembly Instructions: \n" ++ concatMap (\x -> show x ++ "\n") instructions
