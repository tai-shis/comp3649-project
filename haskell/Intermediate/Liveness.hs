module Intermediate.Liveness (
    LivenessState(..),
    LivenessStates,
    showLivenessStates,
    getLivenessName,
    namesFromLiveness,
    isLive,
    isDefined,
    isUnlive,
    determineLiveness,
    livenessInfo,
) where

import Data.Set (
    Set, 
    toList, 
    empty, 
    insert)

import Input.Token (
    Token, 
    TokenType(
        Destination,
        Variable,
        Literal,
        Operator),
    getType, 
    getValue,
    createToken)

import Input.Instruction (
    Instruction, 
    Instructions,
    getVariables, 
    getDestination,
    getInstructions,
    getLiveVariables,
    createInstruction, 
    fromArraysInstructions)

import Lib.Helper (
    commaSperatedList, 
    addList,
    addUnique)

-- Liveness analysis 
type LivenessStates = [LivenessState]

-- Public: Displays the liveness states in a readable format
showLivenessStates :: [LivenessStates] -> String
showLivenessStates liveness = concatMap (\x -> commaSperatedList x ++ "\n" ) liveness

data LivenessState = Defined String 
                   | Live String
                   | Unlive String

instance Eq LivenessState where
    (Defined name1) == (Defined name2) = name1 == name2
    (Live name1) == (Live name2) = name1 == name2
    (Unlive name1) == (Unlive name2) = name1 == name2
    (Defined name1) == (Live name2) = name1 == name2
    (Live name1) == (Defined name2) = name1 == name2
    (Unlive name1) == (Defined name2) = name1 == name2
    (Defined name1) == (Unlive name2) = name1 == name2
    (Live name1) == (Unlive name2) = name1 == name2
    (Unlive name1) == (Live name2) = name1 == name2

instance Show LivenessState where
    show (Defined name) = name ++ ": defined"
    show (Live name) = name ++ ": live"
    show (Unlive name) = name ++ ": unlive"

-- Public: Gets the name of a liveness state
getLivenessName :: LivenessState -> String
getLivenessName (Defined name) = name
getLivenessName (Live name) = name
getLivenessName (Unlive name) = name

-- Public: Takes a list of liveness and returns a list of the variables.
namesFromLiveness :: LivenessStates -> [String]
namesFromLiveness = map getLivenessName

-- Public: Checks if a liveness state is live or defined
isLive :: LivenessState -> Bool
isLive (Live _) = True
isLive _ = False

-- Public: Checks if a liveness state is live or defined
isDefined :: LivenessState -> Bool
isDefined (Defined _) = True
isDefined _ = False

-- Public: Checks if a liveness state is unlive
isUnlive :: LivenessState -> Bool
isUnlive (Unlive _) = True
isUnlive _ = False

-- Private: Convert our end of line "live: " variables into our carry variables
initialLiveness :: Instructions -> LivenessStates
initialLiveness instructions = map (\x -> Live x) (getLiveVariables instructions)

-- Private: Strip the defined variables from the previous liveness state.
stripDefined :: LivenessStates -> LivenessStates
stripDefined liveness = filter (not . isDefined) liveness

-- Private: Given a state thats been defined and the preivous liveness state, remove the live instance of the defined variable.
filterDefined :: String -> LivenessStates -> LivenessStates
filterDefined name liveness = filter (\x -> getLivenessName x /= name) liveness

-- Private: Split instruction into the destination and variables
splitInstruction :: Instruction -> (String, LivenessStates)
splitInstruction instruction = (getValue (getDestination instruction), map (\x -> Live (getValue x)) (getVariables instruction))

-- Private: Given an instruction and previous liveness, generates the new liveness state
markLiveness :: LivenessStates -> String -> LivenessStates -> LivenessStates
markLiveness prevLiveness dest variables | elem dest (namesFromLiveness variables) = addUnlive variables (addUnique (Live dest) prevLiveness)
    | otherwise = addUnlive variables (Defined dest : filterDefined dest prevLiveness)
          

-- Private: adds the last used variables to the current liveness state.
addUnlive :: LivenessStates -> LivenessStates -> LivenessStates
addUnlive [] liveness = liveness
addUnlive (v:vs) liveness | elem v liveness = addUnlive vs liveness
    | otherwise = addUnlive vs (Unlive (getLivenessName v) : liveness)

-- Private: Given previous Liveness, set unlive to live
setAllLive :: LivenessStates -> LivenessStates
setAllLive [] = []
setAllLive (l:ls) = Live (getLivenessName l) : setAllLive ls

-- Private: Given a list of instructions and an initial liveness state, generates a list of liveness states for each instruction
determineRestLiveness :: [Instruction] -> LivenessStates -> [LivenessStates]
determineRestLiveness [] liveness = liveness:[]
determineRestLiveness (instruction:instructions) liveness = liveness : determineRestLiveness instructions newLiveness
    where (dest, variables) = splitInstruction instruction
          previousLiveness = setAllLive (stripDefined liveness)
          newLiveness = markLiveness previousLiveness dest variables

-- Public: Determines the liveness of each instruction in the given Instructions and returns a list of liveness states for each instruction
determineLiveness :: Instructions -> [LivenessStates]
determineLiveness instructions = reverse (determineRestLiveness (reverse (getInstructions instructions)) (initialLiveness instructions))

-- Public: Display the interference table
livenessInfo :: [LivenessStates] -> IO ()
livenessInfo liveness = putStrLn ("Liveness Info: \n" ++ showLivenessStates liveness)