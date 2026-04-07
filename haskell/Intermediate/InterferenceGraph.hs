module Intermediate.InterferenceGraph (
    Variable(..), 
    Graph(..), 
    createVariable, 
    getName, 
    getNeighbors, 
    createGraph, 
    getVertices, 
    addEdge,
    buildGraph,
    -- testBuildGraph,
    -- liveness,
    Register,
    RegisterMap,
    colourGraph,
    -- testColourGraph,
    getColouring
) where

import Lib.Helper (
    commaSperatedList, 
    pairTrue)

import Data.Set (
    Set, 
    toList, 
    empty, 
    insert)

import Intermediate.Liveness (
    LivenessState,
    LivenessStates,
    showLivenessStates,
    getLivenessName,
    namesFromLiveness,
    isLive,
    isDefined,
    isUnlive,
    determineLiveness,
    livenessInfo)

-- for tests
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


type Neighbors = Set String

-- Variables name, and their neighbors (just the names)
data Variable = Var (String, Neighbors)
    deriving (Eq)

instance Show Variable where
    show (Var (name, neighbors)) = name ++ " -> " ++ commaSperatedList (toList neighbors)

data Graph = Graph [Variable]
    deriving (Eq)

instance Show Graph where
    show (Graph vertices) = "Interference Graph: \n" ++ concatMap (\v -> show v ++ "\n") vertices

-- Public: Creates a variable given a name
createVariable :: String -> Variable
createVariable name = Var (name, empty)

-- Public: Gets the name of a variable
getName :: Variable -> String
getName (Var (name, _)) = name

-- Public: Gets the neighbors of a variable 
getNeighbors :: Variable -> Neighbors
getNeighbors (Var (_, neighbors)) = neighbors

-- Public: Creates an empty graph
createGraph :: Graph
createGraph = Graph []

-- Public: Gets the vertices of a graph
getVertices :: Graph -> [Variable]
getVertices (Graph vertices) = vertices

-- Private: Given two variable names, updates the neighbors of a variable if it matches either name
updateNeighbors :: String -> String -> Variable -> Variable
updateNeighbors name1 name2 var = if name == name1 then Var (name, insert name2 neighbors)
    else if name == name2 then Var (name, insert name1 neighbors)
    else var
    where name = getName var
          neighbors = getNeighbors var


-- Private: Checks if two variables exist in the graph
edgeExists :: [Variable] -> String -> String -> (Bool, Bool)
edgeExists [] _ _ = (False, False)
edgeExists (v:vs) name1 name2 | name1 == name2 = (False, False)
    | otherwise = (name == name1 || fst rest, name == name2 || snd rest)
        where rest = edgeExists vs name1 name2
              name = getName v

-- Public: Adds an edge between two variables in the graph if they both exist, otherwise returns the original graph
addEdge :: Graph -> String -> String -> Graph
addEdge graph name1 name2 | pairTrue (edgeExists (getVertices graph) name1 name2) = Graph (map (updateNeighbors name1 name2) (getVertices graph))
    | otherwise = graph


-- Public: Builds the full interference graph from a list of variable names and their liveness states
buildGraph :: [String] -> [LivenessStates] -> Graph
buildGraph variables liveness = foldl (\g (v1, v2) -> addEdge g v1 v2) emptyGraph allPairs
    where emptyGraph = Graph (map createVariable variables)
          activePerLine = map (\line -> map getLivenessName (filter (not . isUnlive) line)) liveness
          allPairs = concatMap getPairs activePerLine

-- Private: Helper function to generate all unique pairs from a list of strings
getPairs :: [String] -> [(String, String)]
getPairs [] = []
getPairs (x:xs) = map (\y -> (x, y)) xs ++ getPairs xs

-- Type alias for better readability and understanding
type Register = Int
-- RegisterMap is the "history" of all the registers that have already been coloured
type RegisterMap = [(String, Register)] 

-- Public: Colours the graph using recursive backtracking
colourGraph :: Graph -> Int -> [RegisterMap]
colourGraph (Graph vars) numColours = solve vars []
    where
        solve :: [Variable] -> RegisterMap -> [RegisterMap]
        solve [] assigned = [assigned]
        solve (v:vs) assigned = 
            -- picks an available register, verifies it doesn't conflict with neighbour, then adds it to finishedMap and keeps going
            [ finishedMap 
            | colour <- [0 .. numColours - 1]
            , isSafe colour v assigned
            , finishedMap <- solve vs ((getName v, colour) : assigned) 
            ]

-- Private: Helper function to check if a register (colour) is safe and does not conflict with neighbours
isSafe :: Register -> Variable -> RegisterMap -> Bool
isSafe colour var assigned = not (any hasConflict assigned)
    where 
        -- list of neighbours that interfere with the variable
        enemies = toList (getNeighbors var)
        -- hasConflict occurs when a previous assigned variable has the same colour and is a neighbour
        hasConflict (enemyName, enemyColour) = (enemyColour == colour) && (elem enemyName enemies)

-- Public: Checks if graph was coloured successfully on runtime, returns the first valid colouring if so.
getColouring :: [RegisterMap] -> RegisterMap
getColouring colourings | length colourings == 0 = error "Graph could not be coloured with the given number of registers" 
                        | otherwise = colourings !! 0
